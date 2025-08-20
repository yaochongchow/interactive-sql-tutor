import os, json
from django.conf import settings
from google.cloud import storage

def load_problem_file(problem_id, filename, parse_json=False):
    folder = str(problem_id).zfill(3)
    local_path = os.path.join(settings.BASE_DIR, "problems", folder, filename)

    # 1. Attempt to load from the local filesystem first
    if os.path.exists(local_path):
        with open(local_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        # 2. If not found, fallback to loading from Google Cloud Storage (GCS)
        client = storage.Client()
        bucket = client.bucket(settings.GCS_PROBLEM_BUCKET)
        blob = bucket.blob(f"problems/{folder}/{filename}")
        if not blob.exists():
            raise FileNotFoundError(f"{filename} not found in local or GCS for problem {problem_id}")
        content = blob.download_as_text()

    # 3. If the file is a JSON file, parse and return it as a Python dictionary
    if parse_json:
        return json.loads(content)
    return content

def get_next_problem_id():
    # Get the maximum problem ID from local filesystem (e.g., /problems/001/, /problems/002/, ...)
    local_root = os.path.join(settings.BASE_DIR, "problems")
    if os.path.exists(local_root):
        local_ids = [
            int(name) for name in os.listdir(local_root)
            if name.isdigit() and os.path.isdir(os.path.join(local_root, name))
        ]
        local_max = max(local_ids, default=0)
    else:
        local_max = 0

    # Get the maximum problem ID from GCS by scanning the 'problems/' folder prefix
    client = storage.Client()
    bucket = client.bucket(settings.GCS_PROBLEM_BUCKET)
    gcs_ids = set()
    for blob in bucket.list_blobs(prefix="problems/"):
        parts = blob.name.split("/")
        if len(parts) > 1 and parts[1].isdigit():
            gcs_ids.add(int(parts[1]))
    gcs_max = max(gcs_ids, default=0)


    return max(local_max, gcs_max) + 1