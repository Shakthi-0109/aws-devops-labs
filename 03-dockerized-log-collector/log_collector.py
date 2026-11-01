import os
import tarfile
import datetime
import boto3
from botocore.exceptions import ClientError

LOG_DIR = os.getenv("APP_LOG_DIR", "/app/logs")
BUCKET_NAME = os.getenv("OFFLOAD_BUCKET_NAME", "devops-logs-offload-shakthi-1147")
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

def generate_mock_logs(directory):
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log_file = os.path.join(directory, "container_service.log")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] [INFO] Container worker transaction processed successfully.\n")
    print(f"[INFO] Diagnostic log entry written to {log_file}")

def compress_and_offload():
    generate_mock_logs(LOG_DIR)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"container_logs_{timestamp}.tar.gz"
    
    with tarfile.open(archive_name, "w:gz") as tar:
        tar.add(LOG_DIR, arcname=os.path.basename(LOG_DIR))
    print(f"[INFO] Archive created: {archive_name}")

    s3_key = f"container-archives/{archive_name}"
    s3_client = boto3.client("s3", region_name=REGION)

    try:
        s3_client.upload_file(
            archive_name,
            BUCKET_NAME,
            s3_key,
            ExtraArgs={"StorageClass": "STANDARD_IA"}
        )
        print(f"[SUCCESS] Shipped to s3://{BUCKET_NAME}/{s3_key}")
        os.remove(archive_name)
        print(f"[STATUS] Local container archive purged successfully.")
    except ClientError as e:
        print(f"[CRITICAL] AWS S3 Upload failed: {e}")

if __name__ == "__main__":
    compress_and_offload()
