Python Library for Deleting Objects in Google Cloud Storage Buckets

This library provides a function clean_up_gcs_bucket that helps you delete unwanted objects from a Google Cloud Storage (GCS) bucket based on a folder path and substring criteria.



** clean_up_gcs_bucket(bucket_name, folder_path, substring): **

The clean_up_gcs_bucket function takes the following arguments:

*Parameters:*

1. bucket_name: (str) The name of the GCS bucket to clean up.
2. folder_path (str, optional): An optional prefix to filter objects within a specific folder path in the bucket. Include a trailing slash. Defaults to listing all objects in the bucket.
3. substring (str, optional): An optional substring to filter objects. Objects containing the substring (case-insensitive) will be deleted. Defaults to deleting all objects matching the folder_path criteria.



*Example Usage:*

```Python

from clean_up_gcs_bucket import clean_up_gcs_bucket

# Replace with your information
bucket_name = "your-bucket-name"
folder_path = "path/to/your/folder/"  # Optional, defaults to all files in bucket
substring = "report"  # Optional, deletes objects containing the substring (case-insensitive)

clean_up_gcs_bucket(bucket_name, folder_path, substring)

```


*Function Behavior*
1. Connects to GCS using storage.Client.
2. Retrieves the bucket specified by bucket_name.
3. Lists all blobs (objects) in the bucket, optionally filtered by folder_path.
4. Iterates through each file in the bucket: 
    a). Checks if the substring is provided: 
        1. If not provided, all objects matching the folder_path (if    specified) will be deleted.
        2. If provided, objects containing the substring (case-insensitive) and matching the folder_path (if specified) will be deleted.
    b). Deletes the matching blob using blob.delete().
    c). Keeps a count of deleted objects.
5. Prints a summary message indicating the number of deleted objects, bucket name, folder path (if provided), and the used substring (if provided).


**Additional Notes:**

1. This function permanently deletes objects from GCS. Use caution and ensure you have backups if necessary.
2. Be specific with folder_path and substring to avoid unintended deletions.
3. This library uses the google-cloud-storage library. Ensure it is installed (pip install google-cloud-storage).

