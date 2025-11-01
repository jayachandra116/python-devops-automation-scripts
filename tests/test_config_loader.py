from utils.config_loader import load_config


def test_load_config():
    config = load_config()
    assert isinstance(config, dict)
    assert "aws" in config
