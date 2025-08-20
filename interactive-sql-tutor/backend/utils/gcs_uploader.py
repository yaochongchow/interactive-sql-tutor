from django.conf import settings
from google.cloud import storage

def upload_problem_to_gcs(problem_id: int, files: dict):
    folder = str(problem_id).zfill(3)
    client = storage.Client()
    bucket = storage.Client().bucket(settings.GCS_PROBLEM_BUCKET)

    for filename, content in files.items():
        blob = bucket.blob(f"problems/{folder}/{filename}")
        blob.upload_from_string(content, content_type="text/plain")