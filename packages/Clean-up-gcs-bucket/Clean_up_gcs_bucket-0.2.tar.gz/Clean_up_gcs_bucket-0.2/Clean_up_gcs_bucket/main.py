from google.cloud import storage

def clean_up_gcs_bucket(bucket_name, folder_path='', substring=''):
    # Create a client to interact with Google Cloud Storage
    client = storage.Client()

    # Get the bucket
    bucket = client.get_bucket(bucket_name)

    # List all blobs in the bucket
    blobs = bucket.list_blobs(prefix=folder_path)

    # Delete blobs matching the folder_path and substring condition
    deleted_count = 0
    for blob in blobs:
        if not substring or substring.lower() in blob.name.lower():
            blob.delete()
            deleted_count += 1

    print(f"Deleted {deleted_count} file(s) in bucket {bucket_name} within folder {folder_path} and containing substring '{substring}'.")
