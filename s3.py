'''
Create a bucket and upload a file to it.
Download an object from a bucket.
Copy an object to a subfolder in a bucket.
List the objects in a bucket.
Delete the bucket objects and the bucket.

'''

import io  # common task in Python for input/output operations. 
import uuid
import os
import boto3
from boto3.s3.transfer import S3UploadFailedError
from botocore.exceptions import ClientError


def my_function(s3_resource):
    print("Amazon S3 demo starting now")

  
    bucket_name = f'my-bucket-{uuid.uuid(4)}'  # uuid4() creates a random UUID.
    bucket = s3_resource.Bucket(bucket_name)

    try:   # Creating the AWS S3 Bucket
        bucket.create(
            CreateBucketConfiguration={
                "LocationConstraint": s3_resource.meta.client.meta.region_name
            }
        )
        print(f"Created demo bucket named {bucket.name}.")    
    
    except ClientError as err:  #  Error if Bucket is not created
        print(f"Tried and failed to create demo bucket {bucket_name}.")
        print(f"\t{err.response['Error']['Code']}:{err.response['Error']['Message']}")
        print(f"\nCan't continue the demo without a bucket!")
        return
    
    file_name = None  # Checking the files Locally to upload in the AWS S3 Bucket
    while file_name is None:
        file_name = input("Enter file to upload")
        if not os.path.exists(file_name):
            print(f"Couldn't find file {file_name}. Are you sure it exists?")
            file_name = None
    
    obj = bucket.Object(os.path.basename(file_name)) # Uploading the files in the AWS S3 Bucket
    try:
         obj.upload_file(file_name)
         print( f"Uploaded file {file_name} into bucket {bucket.name} with key {obj.key}.")
    except S3UploadFailedError as err:
            print(f"Couldn't upload file {file_name} to {bucket.name}.")
            print(f"\t{err}")    
    
    download = input("what you want to download")   # Downloading the files in the AWS S3 Bucket
    if download.lower() == "y":
         data = io.BytesIO()    # It can be used as a file-like object for reading and writing binary data.
         try: 
            obj.download_fileobj(data)
            data.seek(0) # Move to the start of the buffer
            print(f"Got your object. Here are the first 20 bytes:\n")
            print(f"\t{data.read(20)}")
         except ClientError as err:
            print(f"Couldn't download {obj.key}.")
            print(f"\t{err.response['Error']['Code']}:{err.response['Error']['Message']}")  
    
    copy = input("what you want to copy")   # Downloading the files in the AWS S3 Bucket
    if copy.lower() == "y":
         dest_obj = bucket.Object(f"demo-folder"/{obj.key}) # Uploading the files in the AWS S3 Bucket
         try:
            dest_obj.copy({"Bucket":bucket.name,"Key":obj.key})
            print(f"Copied {obj.key} to {dest_obj.key}.")
         except ClientError as err:
            print(f"Couldn't copy {obj.key} to {dest_obj.key}.")
            print(f"\t{err.response['Error']['Code']}:{err.response['Error']['Message']}")
    
    print("Listing the objects in the bucket")
    try:
        for i in bucket.objects.all():
            print(f"\t{i.key}")
    except ClientError as err:
            print(f"Couldn't list the objects in bucket {bucket.name}.")
            print(f"\t{err.response['Error']['Code']}:{err.response['Error']['Message']}")

    print("Deleting the objects in the bucket & finally the bucket")
    try:
            bucket.objects.delete()
            bucket.delete()
            print(f"Emptied and deleted bucket {bucket.name}.\n")
    except ClientError as err:
            print(f"Couldn't empty and delete bucket {bucket.name}.")        

if __name__ == "__main__":
    my_function(boto3.resource("s3"))
