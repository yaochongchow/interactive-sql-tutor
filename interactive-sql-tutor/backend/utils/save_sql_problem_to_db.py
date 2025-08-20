def save_sql_problem_to_db(cursor, metadata: dict):
    """
    Save SQL problem metadata to the SQLProblem and Hint tables in the MySQL database.

    This function performs two main tasks:
    1. Inserts or updates the SQLProblem record using the provided metadata.
       - If a problem with the same `problem_id` already exists, it will be updated.
       - Otherwise, a new record will be created.
    2. Deletes any existing hints for the given `problem_id`, and inserts new hints
       based on the metadata.

    Args:
        cursor (MySQLCursor): The MySQL database cursor object used for executing SQL statements.
        metadata (dict): A dictionary parsed from `metadata.json` that includes:
            - problem_id (int): Unique ID of the problem
            - title (str): Title of the SQL problem
            - description (str): Problem description text
            - difficulty_level (str): One of ['Easy', 'Medium', 'Hard', 'Expert']
            - topic_id (int): Foreign key referring to a Topic
            - hints (list[str], optional): A list of hint strings associated with the problem

    Returns:
        None

    Example:
        metadata = {
            "problem_id": 1,
            "title": "Top Sales by Employee",
            "description": "Find the product with the highest sales for each employee.",
            "difficulty_level": "Medium",
            "topic_id": 2,
            "hints": [
                "Use GROUP BY to aggregate sales per employee.",
                "Use a subquery or window function to get the top product."
            ]
        }
        save_sql_problem_to_db(cursor, metadata)
    """
    # Insert or update SQLProblem table
    insert_sqlproblem = """
        INSERT INTO SQLProblem (problem_id, title, description, difficulty_level, topic_id)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            description = VALUES(description),
            difficulty_level = VALUES(difficulty_level),
            topic_id = VALUES(topic_id)
    """
    cursor.execute(insert_sqlproblem, (
        metadata["problem_id"],
        metadata["title"],
        metadata["description"],
        metadata["difficulty_level"],
        metadata["topic_id"]
    ))

    # Clear existing hints
    delete_hints = "DELETE FROM Hint WHERE problem_id = %s"
    cursor.execute(delete_hints, (metadata["problem_id"],))

    # Insert new hints
    insert_hint = """
        INSERT INTO Hint (problem_id, hint_text, hint_order)
        VALUES (%s, %s, %s)
    """
    for i, hint in enumerate(metadata.get("hints", []), start=1):
        cursor.execute(insert_hint, (
            metadata["problem_id"],
            hint,
            i
        ))