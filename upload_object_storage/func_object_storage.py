import logging
from botocore.exceptions import ClientError

def list_files(s3_client, bucket):
    """
    Function to list files in a given Object Storage bucket
    """
    file_names = []
    for item in s3_client.list_objects(Bucket=bucket)['Contents']:
        file_names.append(item)

    return file_names

def upload_file(s3_client, file_name, bucket, object_name=None):
    """
    Function to upload a file to an Object Storage bucket
    """
    if object_name is None:
        object_name = file_name
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True