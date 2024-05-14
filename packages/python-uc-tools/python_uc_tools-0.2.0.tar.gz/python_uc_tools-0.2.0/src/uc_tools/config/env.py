from __future__ import annotations

from dataclasses import fields
from pathlib import Path


class BaseConfig:
    """
    Abstract base class for the application configuration.

    It's used to define the structure of the application configuration
    and validate the environment variables.
    """


class Env:
    @staticmethod
    def find_env(env_name: str) -> Path:
        """
        Find the environment file in the current or root project directory.
        """
        current_dir = Path.cwd()
        env_files = [
            current_dir / env_name,
            current_dir.parent / env_name,
            current_dir.parent.parent / env_name,
        ]
        for env_file in env_files:
            if env_file.exists():
                return env_file
        msg = f'Cannot find {env_name} file in the current or root project directory.'
        raise FileNotFoundError(
            msg
        )

    @classmethod
    def load(
        cls,
        env_name: str = '.env',
        config: type[BaseConfig] | None = None,
    ) -> BaseConfig:
        """
        Load environment variables from the environment file.

        Args:
            environment_file (str | None): The path to the environment file.

        Returns:
            Settings: The loaded settings.

        Raises:
            ValueError: If a setting is missing or has an invalid type.
        """
        settings_dict: dict[str, str | int] = {}
        env_file = cls.find_env(env_name)

        with Path.open(env_file, 'r') as f:
            for line in f:
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith('#'):
                    key, value = map(str.strip, stripped_line.split('='))
                    try:
                        value = int(value)
                    except ValueError:
                        value = value or ''
                    settings_dict[key.lower()] = value

        for field in fields(config):
            if field.name.lower() not in settings_dict:
                msg = f'Missing setting: {field.name}'
                raise ValueError(msg)
            if field.type is not type(settings_dict[field.name]) and field.type is not str:
                msg = f'Invalid type for setting: {field.name}. Expected {field.type}, got {type(settings_dict[field.name])}'
                raise ValueError(
                    msg
                )

        return config(**settings_dict)
