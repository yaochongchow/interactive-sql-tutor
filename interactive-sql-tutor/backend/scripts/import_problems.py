import os
import json
import mysql.connector

import sys
import os
import django

# Ensure the project root directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Explicitly specify the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_project.settings")

# Initialize the Django application environment
django.setup()

from config.db_config import get_mysql_db_config
print("DJANGO_SETTINGS_MODULE:", os.environ.get('DJANGO_SETTINGS_MODULE'))

# This script imports SQL problem metadata into the database by reading JSON files 
# from each subfolder in the `problems` directory.

# Purpose:
# - Insert or update SQLProblem records based on metadata.json files.
# - Delete and reinsert associated hints from the same metadata file.

# Assumptions:
# - Each subfolder in `problems/` represents one problem (e.g., 001/, 002/).
# - Each folder contains a `metadata.json` file with the problem's info and hints.
# - The MySQL database contains tables: SQLProblem and Hint.
# - `ON DUPLICATE KEY UPDATE` is used to ensure idempotent imports.

# Folder containing problem definitions
PROBLEMS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "problems")
db_config = get_mysql_db_config()

# Connect to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Iterate through each problem folder (e.g., "001", "002", etc.)
for problem_folder in sorted(os.listdir(PROBLEMS_DIR)):
    folder_path = os.path.join(PROBLEMS_DIR, problem_folder)
    metadata_path = os.path.join(folder_path, "metadata.json")

    if os.path.isfile(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            ## Insert or update the SQLProblem record
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
                data["problem_id"],
                data["title"],
                data["description"],
                data["difficulty_level"],
                data["topic_id"]
            ))

            # Clear old hints for this problem
            delete_hints = "DELETE FROM Hint WHERE problem_id = %s"
            cursor.execute(delete_hints, (data["problem_id"],))
            # Insert new hints (ordered)
            insert_hint = """
                INSERT INTO Hint (problem_id, hint_text, hint_order)
                VALUES (%s, %s, %s)
            """
            for i, hint in enumerate(data.get("hints", []), start=1):
                cursor.execute(insert_hint, (
                    data["problem_id"],
                    hint,
                    i
                ))

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()