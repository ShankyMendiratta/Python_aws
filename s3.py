# Creates a bucket and upload a file to it.
# Downloads an object from a bucket.
# Copies an object to a subfolder in a bucket.
# Lists the objects in a bucket.
# Deletes the bucket objects and the bucket.


import io # 
import os
import uuid # The UUID module offers the ability to produce distinctive IDs in accordance with the RFC 4122 definition
import boto3
from botocore.exceptions import ClientError

