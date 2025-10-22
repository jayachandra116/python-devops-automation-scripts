# Python DevOps Automation Scripts 🧩

A collection of Python scripts for automating everyday DevOps tasks — from AWS operations and Docker health checks to CI/CD pipeline triggers.

---

## 🧱 Features
- AWS EC2/S3/IAM management via boto3
- Docker container monitoring
- Disk usage alerts
- Trigger GitHub workflows via API
- Logging & config management
- CI/CD integration using GitHub Actions

---
## ⚙️ Setup

```bash
git clone https://github.com/jayachandra116/python-devops-automation-scripts.git
cd python-devops-automation-scripts
pip install -r requirements.txt

## ☁️ AWS Automation Scripts

### `ec2_monitor.py`
Monitors running EC2 instances and checks CPU utilization using CloudWatch metrics.

### `s3_manager.py`
Uploads, downloads, and lists S3 bucket files, skipping existing ones.

### `iam_audit.py`
Audits IAM users and flags inactive users (no access key use for 90+ days).

Run examples:
```bash
python scripts/aws/ec2_monitor.py
python scripts/aws/s3_manager.py
python scripts/aws/iam_audit.py