import datetime
import boto3
from utils.config_loader import load_config
from utils.logger import get_logger


logger = get_logger(__name__)
config = load_config()

REGION = config.get("aws", {}).get("region", "us-east-1")
CPU_THRESHOLD = config.get("aws", {}).get("cpu_threshold", 80)


def get_ec2_instances():
    """Return list of running EC2 instance IDs."""
    ec2_client = boto3.client("ec2", region_name=REGION)
    instances = ec2_client.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )
    instance_ids = []
    for reservation in instances["Reservations"]:
        for instance in reservation["Instances"]:
            instance_ids.append(instance["InstanceId"])

    return instance_ids


def get_cpu_utilization(instance_id):
    """Get avg CPU utilization of an instance in the last 10min."""
    cloudwatch = boto3.client("cloudwatch", region_name=REGION)
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(minutes=10)

    metrics = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average"],
    )

    datapoints = metrics.get("Datapoints", [])
    if not datapoints:
        return 0.0
    return datapoints[-1]["Average"]


def main():
    logger.info("Starting EC2 monitoring ...")
    instances = get_ec2_instances()

    if not instances:
        logger.info("No running EC2 instances found.")
        return

    for instance_id in instances:
        cpu = get_cpu_utilization(instance_id)
        logger.info(f"Instance {instance_id} CPU Utilization: {cpu:.2f}%")

        if cpu > CPU_THRESHOLD:
            logger.warning(f"High CPU alert: {instance_id} exceeds {CPU_THRESHOLD}%")

    logger.info("EC2 monitoring complete.")


if __name__ == "__main__":
    main()
