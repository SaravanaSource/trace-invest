from pathlib import Path
import yaml
from typing import Dict, Any

CONFIG_DIR = Path("configs")


class ConfigError(Exception):
    """Raised when configuration is invalid or missing."""


def _load_yaml(file_path: Path) -> Dict[str, Any]:
    if not file_path.exists():
        raise ConfigError(f"Missing config file: {file_path.name}")

    with file_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_config() -> Dict[str, Any]:
    """
    Loads and validates all system configuration files.
    This is the single source of truth for the system.
    """
    config_files = [
        "system.yaml",
        "universe.yaml",
        "risk.yaml",
        "data_sources.yaml",
    ]

    config: Dict[str, Any] = {}

    for filename in config_files:
        data = _load_yaml(CONFIG_DIR / filename)
        key = filename.replace(".yaml", "")
        config[key] = data

    _validate_config(config)
    return config


def _validate_config(config: Dict[str, Any]) -> None:
    required_keys = [
        "system",
        "universe",
        "risk",
        "data_sources",
    ]

    for key in required_keys:
        if key not in config or not config[key]:
            raise ConfigError(f"Invalid or empty config section: {key}")

