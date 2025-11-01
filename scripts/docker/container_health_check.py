import docker
from utils.logger import get_logger
from utils.config_loader import load_config

logger = get_logger(__name__)
config = load_config()

CPU_THRESHOLD = config.get("docker", {}).get("cpu_threshold", 80)
MEMORY_THRESHOLD = config.get("docker", {}).get("memory_threshold", 80)


def get_container_stats(container):
    """Return container CPU and memory usage as percentage."""
    stats = container.stats(stream=False)
    cpu_delta = (
        stats["cpu_stats"]["cpu_usage"]["total_usage"]
        - stats["precpu_stats"]["cpu_usage"]["total_usage"]
    )
    system_delta = (
        stats["cpu_stats"]["system_cpu_usage"]
        - stats["precpu_stats"]["system_cpu_usage"]
    )

    cpu_percent = 0.0
    # pprint.pprint(stats)
    if system_delta > 0.0:
        cpu_percent = (
            (cpu_delta / system_delta)
            * stats["cpu_stats"]["online_cpus"]
            * 100.0
        )

    mem_usage = stats["memory_stats"].get("usage", 0)
    mem_limit = stats["memory_stats"].get("limit", 1)
    mem_percent = (mem_usage / mem_limit) * 100.0

    return cpu_percent, mem_percent


def main():
    client = docker.from_env()
    containers = client.containers.list()

    if not containers:
        logger.info("No running containers found.")
        return

    logger.info("Checking container health...")
    for container in containers:
        cpu, mem = get_container_stats(container)
        logger.info(
            f"{container.name}: CPU={cpu:.2f}% | Memory={mem:.2f}%"
        )

        if cpu > CPU_THRESHOLD:
            logger.warning(
                f"High CPU alert for {container.name}: {cpu:.2f}%"
            )
        if mem > MEMORY_THRESHOLD:
            logger.warning(
                f"High memory alert for {container.name}: {mem:.2f}%"
            )

    logger.info("Docker container health check complete.")


if __name__ == "__main__":
    main()
