########### Lambda code to upload file to s3 with data appending on same date when lambda triggers with the SQS #############
import json
from time import strftime
import boto3
s3 = boto3.client("s3")

def s3_upload(data):
    new=data
    file_name="newlog"
    with open("/tmp/"+ file_name, "a+") as f:
        f.write("\n"+ "=============="+ strftime("%H:%M:%S") + "==============" + "\n")
        f.write(new)
    s3.upload_file("/tmp/"+file_name, "bucket-name", strftime("%B-%d-%Y"))
    
    
def lambda_handler(event,context):
    s3_upload("event")
