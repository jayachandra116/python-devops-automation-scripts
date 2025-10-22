import boto3
from datetime import datetime, timezone
from utils.logger import get_logger
from utils.config_loader import load_config

logger = get_logger(__name__)
config = load_config()

iam = boto3.client("iam")
INACTIVE_DAYS = 90


def audit_iam_users():
    """List IAM users and check for inactivity"""
    users = iam.list_users()["Users"]
    now = datetime.now(timezone.utc)

    for user in users:
        username = user["UserName"]
        keys = iam.list_access_keys(UserName=username)["AccessKeyMetadata"]
        if not keys:
            logger.info(f"{username}: No access keys.")
            continue

        for key in keys:
            last_used = iam.get_access_key_last_used(AccessKeyId=key["AccessKeyId"])
            last_used_date = last_used["AccessKeyLastUsed"].get("LastUsedDate")
            if not last_used_date:
                logger.warning(f"{username}: Access key never used.")
                continue

            days_inactive = (now - last_used_date).days
            if days_inactive > INACTIVE_DAYS:
                logger.warning(f"{username} inactive for {days_inactive} days.")
            else:
                logger.info(f"{username}: Active ({days_inactive} days since last use)")


def main():
    logger.info("Starting IAM audit ...")
    audit_iam_users()
    logger.info("IAM audit complete.")


if __name__ == "__main__":
    main()
