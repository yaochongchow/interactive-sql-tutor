import uuid
from contextlib import contextmanager
import mysql.connector
import os
from config.db_config import get_mysql_db_config
from django.conf import settings
import json
from utils.problem_loader import load_problem_file

@contextmanager
def sandbox_schema(db_config):
    """
    Context manager to create a temporary MySQL schema (database) 
    for isolated SQL execution (sandboxing).

    This is useful when you want to:
    - Run user-submitted SQL queries in a safe, isolated environment
    - Avoid affecting your main database
    - Automatically clean up after execution

    Behavior:
    1. Creates a uniquely named schema using UUID (e.g., 'sandbox_a1b2c3d4')
    2. Switches to that schema using 'USE'
    3. Yields a live database connection, cursor, and the schema name for use within the `with` block
    4. Automatically drops the schema after the block completes, even on error

    Parameters:
        db_config (dict): A dictionary of MySQL database connection settings, 
                          typically containing host, user, password, and port.

    Yields:
        tuple: (conn, cursor, schema_name)
            - conn: Active MySQL connection object
            - cursor: Cursor for executing SQL queries
            - schema_name: The temporary schema name created

    Example:
        with sandbox_schema(db_config) as (conn, cursor, schema_name):
            cursor.execute("CREATE TABLE test (id INT)")
            cursor.execute("INSERT INTO test (id) VALUES (1)")
            cursor.execute("SELECT * FROM test")
            print(cursor.fetchall())

        # After the block, the sandbox schema is dropped automatically.
    """
    schema_name = f"sandbox_{uuid.uuid4().hex[:8]}"  # Generate a unique schema name
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        cursor.execute(f"CREATE SCHEMA `{schema_name}`") # Create sandbox schema
        cursor.execute(f"USE `{schema_name}`")           # Switch to sandbox schema
        yield conn, cursor, schema_name                  # Provide context to caller
    finally:
        cursor.execute(f"DROP SCHEMA IF EXISTS `{schema_name}`") # Clean up schema
        cursor.close()
        conn.close()

def run_problem_setup(cursor, problem_id):
    """
    Executes DDL and INSERT statements to set up the problem's database schema and test data.

    This function should be used after establishing a sandbox environment using `sandbox_schema`.

    Steps:
    1. Verifies that the provided SQL file exists.
    2. Reads the SQL file content (UTF-8 encoded).
    3. Splits the content by semicolon (`;`) to handle multiple SQL statements.
    4. Executes each non-empty SQL statement using the provided cursor.

    Parameters:
        cursor (MySQLCursor): An active cursor connected to the sandbox schema.
        ddl_sql_path (str): The path to the .sql file containing table creation and test data insertion statements.

    Raises:
        FileNotFoundError: If the specified SQL file does not exist.

    Example usage:
        with sandbox_schema(db_config) as (conn, cursor, schema_name):
            run_problem_setup(cursor, "problems/001/setup.sql")
    """
    ddl_sql = load_problem_file(problem_id, "problem.sql")  # return as str

    for statement in ddl_sql.split(';'):
        stmt = statement.strip()
        if stmt:
            cursor.execute(stmt)

def get_solution_output(cursor, problem_id):
    """
    Executes the provided solution SQL file and returns the expected output as a list of dictionaries.

    This function is typically used to retrieve the reference (correct) output for a SQL problem,
    which will later be compared to the user's query result.

    Steps:
    1. Verifies that the solution SQL file exists.
    2. Reads the SQL query from the file (UTF-8 encoded).
    3. Executes the query using the provided cursor.
    4. Fetches all results and converts each row to a dictionary using column names as keys.

    Parameters:
        cursor (MySQLCursor): An active cursor connected to the sandbox schema.
        solution_sql_path (str): Path to the solution.sql file containing the correct SQL query.

    Returns:
        List[Dict]: Query result as a list of dictionaries where each dictionary represents one row.

    Raises:
        FileNotFoundError: If the specified SQL file does not exist.

    Example usage:
        with sandbox_schema(db_config) as (conn, cursor, schema_name):
            expected_output = get_solution_output(cursor, "problems/001/solution.sql")
    """
    solution_sql = load_problem_file(problem_id, "solution.sql")

    cursor.execute(solution_sql)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def check_user_query(problem_id, user_query):
    """
    Validates a user's SQL query by comparing its result with the expected output.

    Features:
    - Checks for forbidden SQL operations (e.g., INSERT, DELETE, DROP).
    - Supports multiple SQL statements; only the result of the final SELECT is compared.
    - Runs the query in an isolated sandbox schema to ensure safety.
    - Loads the expected output from `solution.sql` and compares it against the user's result.
    - Optionally considers result ordering, based on `metadata.json`.

    Steps:
    1. Block dangerous SQL operations for safety.
    2. Set up the sandbox environment using the problem's DDL and test data.
    3. Parse and execute the user's SQL statements.
       - Only SELECT/CTE results are captured.
    4. Fetch and compare the output against the reference solution.
    5. Return a boolean for correctness and an optional message.

    Parameters:
        problem_id (int): The ID of the SQL problem (e.g., 1, 2, 3...).
        user_query (str): The SQL code submitted by the user.

    Returns:
        (bool, str): A tuple indicating:
            - Whether the query output is correct
            - A message describing the error or mismatch (empty string if correct)

    Example return values:
        (True, "")                             # Query is correct
        (False, "Output does not match...")    # Result is wrong
        (False, "Query contains forbidden...") # Dangerous SQL detected
        (False, "Error in query execution: ...") # Runtime error
    """
    forbidden_keywords = ['insert', 'delete', 'update', 'drop', 'alter']

    # Check for forbidden operations
    lowered = user_query.lower()
    if any(kw in lowered for kw in forbidden_keywords):
        return False, "Query contains forbidden SQL operation."

    try:
        db_config = get_mysql_db_config()
        with sandbox_schema(db_config) as (conn, cursor, _):
            # 1. Setup sandbox: schema + test data
            run_problem_setup(cursor, problem_id)

            # 2. Load metadata.json
            try:
                metadata = load_problem_file(problem_id, "metadata.json", parse_json=True)
                requires_order = metadata.get("requires_order", False)
            except FileNotFoundError:
                requires_order = False

            # 3. Execute user's query
            statements = [stmt.strip() for stmt in user_query.strip().split(';') if stmt.strip()]
            if not statements:
                return False, "No valid SQL statement provided."

            user_result = None
            for stmt in statements:
                try:
                    cursor.execute(stmt)
                    if stmt.lower().startswith("select") or stmt.lower().startswith("with"):
                        columns = [col[0] for col in cursor.description]
                        user_result = [dict(zip(columns, row)) for row in cursor.fetchall()]
                except Exception as e:
                    return False, f"Error in query execution: {str(e)}"

            if user_result is None:
                return False, "No SELECT result found from user query."

            # 4. Get expected output
            solution_result = get_solution_output(cursor, problem_id)

            # 5. Optional: ignore order
            if not requires_order:
                user_result = sorted(user_result, key=lambda x: tuple(x.values()))
                solution_result = sorted(solution_result, key=lambda x: tuple(x.values()))

            if user_result == solution_result:
                return True, ""
            else:
                return False, "Output does not match expected result."

    except Exception as e:
        return False, f"Execution error: {str(e)}"