import shutil
import psutil
from utils.logger import get_logger
from utils.config_loader import load_config

logger = get_logger(__name__)
config = load_config()

DISK_THRESHOLD = config.get("system", {}).get("disk_alert_threshold", 80)


def check_disk_usage(path="/"):
    """Check disk usage and log alerts."""
    total, used, free = shutil.disk_usage(path)
    percent_used = (used / total) * 100

    logger.info(f"Disk usage for {path}: {percent_used:.2f}% used")
    if percent_used > DISK_THRESHOLD:
        logger.warning(f"⚠️ Disk usage exceeds threshold ({DISK_THRESHOLD}%) on {path}")


def check_memory_usage():
    """Check system memory usage."""
    mem = psutil.virtual_memory()
    percent_used = mem.percent

    logger.info(f"Memory usage: {percent_used:.2f}% used")
    if percent_used > DISK_THRESHOLD:
        logger.warning(f"⚠️ Memory usage exceeds threshold ({DISK_THRESHOLD}%)")


def main():
    logger.info("Running system health checks...")
    check_disk_usage("/")
    check_memory_usage()
    logger.info("System health check complete.")


if __name__ == "__main__":
    main()
