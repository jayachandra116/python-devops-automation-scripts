from pathlib import Path
import yaml


def load_config(config_path: str = "configs/config.yaml") -> dict:
    """Loads the yaml config file

    Args:
        config_path (str): Config file to load

    Returns:
        dict: Config
    """
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    with open(config_file, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config
