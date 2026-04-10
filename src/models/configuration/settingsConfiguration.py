from __future__ import annotations

from dataclasses import dataclass

from src.models.configuration.availablePrefixConfiguration import PrefixConfiguration
from src.models.configuration.csvFileConfiguration import CsvFileConfiguration
from src.models.configuration.keysSheetConfiguration import KeysSheetConfiguration
from src.models.configuration.languageConfiguration import LanguageConfiguration
from src.models.configuration.pathsConfiguration import PathsConfig


@dataclass
class SettingsConfig:
    """Agrupa toda la configuración principal de la aplicación."""

    languages: list[LanguageConfiguration]
    """Listado de idiomas disponibles."""

    csvFile: CsvFileConfiguration
    """Configuración del archivo CSV."""

    paths: PathsConfig
    """Configuración de rutas de entrada y salida."""

    keysSheet: KeysSheetConfiguration
    """Configuración específica para la hoja de claves (keys sheet)"""    

    localePrefixes: list[PrefixConfiguration]
    """Listado de prefijos permitidos para filtrar contenidos."""