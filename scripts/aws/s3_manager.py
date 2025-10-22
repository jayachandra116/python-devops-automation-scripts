import boto3
from pathlib import Path
from utils.logger import get_logger
from utils.config_loader import load_config

logger = get_logger(__name__)
config = load_config()

REGION = config.get("aws", {}).get("region", "us-east-1")
BUCKET_NAME = config.get("aws", {}).get("s3_bucket", "example-bucket")

s3 = boto3.client("s3", region_name=REGION)


def list_files():
    """List files in S3 bucket."""
    try:
        objects = s3.list_objects_v2(Bucket=BUCKET_NAME)
        files = []
        for content in objects.get("Contents", []):
            files.append(content["Key"])
        logger.info(f"Files in {BUCKET_NAME}: {files}")
        return files
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        return []


def upload_file(local_path: str, s3_key: str):
    """Upload file to S3 if it doesn't already exist."""
    files = list_files()
    if s3_key in files:
        logger.info(f"Skipping upload. File already exists: {s3_key}")
        return

    try:
        s3.upload_file(local_path, BUCKET_NAME, s3_key)
        logger.info(f"Uploaded {local_path} to s3://{BUCKET_NAME}/{s3_key}")
    except Exception as e:
        logger.error(f"Upload failed: {e}")


def download_file(s3_key: str, local_path: str):
    """Download file from S3 if not already downloaded."""
    local_path = Path(local_path)
    if local_path.exists():
        logger.info(f"Skipping download. File already exists: {local_path}")
        return

    try:
        s3.download_file(BUCKET_NAME, s3_key, str(local_path))
        logger.info(f"Downloaded {s3_key} to {local_path}")
    except Exception as e:
        logger.error(f"Download failed: {e}")


def main():
    logger.info("Running S3 Manager")
    logger.info("Listing files ...")
    list_files()
    # upload_file("data.txt", "data.txt")
    # download_file("data.txt", "logs/data.txt")


if __name__ == "__main__":
    main()
