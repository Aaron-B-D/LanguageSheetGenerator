from dataclasses import dataclass

from src.models.configuration.settingsConfiguration import SettingsConfig


@dataclass
class AppConfiguration:
    """Representa el archivo de configuración completo de la aplicación."""

    settings: SettingsConfig
    """Bloque principal de configuración."""