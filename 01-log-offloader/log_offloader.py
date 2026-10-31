import os
import tarfile
import datetime
import boto3
from botocore.exceptions import ClientError

# Configuration
LOG_DIR = os.getenv("APP_LOG_DIR", "./sample_logs")
BUCKET_NAME = os.getenv("OFFLOAD_BUCKET_NAME", "devops-logs-offload-shakthi-1147")
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
def create_sample_logs():
    """Simulates production application generating log files"""
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(os.path.join(LOG_DIR, "app.log"), "a") as f:
        f.write(f"[ERROR] {datetime.datetime.now()} - Database connection pool exhausted on port 5432\n")
    with open(os.path.join(LOG_DIR, "system.log"), "a") as f:
        f.write(f"[WARN] {datetime.datetime.now()} - Root partition disk usage crossed 85%\n")
    print("[INFO] Sample application logs generated.")

def compress_logs(archive_name):
    """Packs and compresses the log directory into a tar.gz archive"""
    print(f"[INFO] Compressing {LOG_DIR} into {archive_name}...")
    with tarfile.open(archive_name, "w:gz") as tar:
        tar.add(LOG_DIR, arcname=os.path.basename(LOG_DIR))
    print(f"[INFO] Compression complete: {archive_name}")

def upload_and_clean(archive_name):
    """Uploads archive to S3 with STANDARD_IA tier and reclaims local disk space"""
    s3_client = boto3.client("s3", region_name=REGION)
    s3_key = f"archived-logs/{archive_name}"
    
    try:
        print(f"[INFO] Uploading {archive_name} to s3://{BUCKET_NAME}/{s3_key} (STANDARD_IA)...")
        s3_client.upload_file(
            Filename=archive_name,
            Bucket=BUCKET_NAME,
            Key=s3_key,
            ExtraArgs={"StorageClass": "STANDARD_IA"}
        )
        print("[SUCCESS] Archive verified and uploaded to S3.")

        # Reclaim disk space only after confirmed upload
        if os.path.exists(archive_name):
            os.remove(archive_name)
            print(f"[STATUS] Local archive {archive_name} purged. Disk space reclaimed.")

    except ClientError as e:
        print(f"[CRITICAL] AWS Upload failed: {e}")
        print("[WARNING] Local file retained for data safety.")

if __name__ == "__main__":
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_file = f"logs_{timestamp}.tar.gz"

    create_sample_logs()
    compress_logs(archive_file)
    upload_and_clean(archive_file)