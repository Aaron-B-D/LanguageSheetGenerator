from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from src.models.configuration.appConfiguration import AppConfiguration
from src.models.configuration.availablePrefixConfiguration import PrefixConfiguration
from src.models.configuration.csvFileConfiguration import CsvFileConfiguration
from src.models.configuration.keysSheetConfiguration import KeysSheetConfiguration
from src.models.configuration.languageConfiguration import LanguageConfiguration
from src.models.configuration.pathsConfiguration import PathsConfig
from src.models.configuration.settingsConfiguration import SettingsConfig


CONFIG_FILE_NAME = "lsg.json"
CONFIG_RELATIVE_PATH = Path("config") / CONFIG_FILE_NAME

JsonDict = dict[str, Any]


class ConfigurationUtils:
    """Carga y expone la configuración de la aplicación desde un archivo JSON."""

    app_config: AppConfiguration | None = None
    input_csv_path: Path | None = None;
    input_csv_file_path: Path;


    @classmethod
    def get_config_path(cls) -> Path:
        return Path(__file__).resolve().parent.parent.parent / CONFIG_RELATIVE_PATH

    @classmethod
    def load_configuration(cls) -> None:
        """Carga la configuración desde el archivo JSON y la almacena en app_config."""
        config_path = cls.get_config_path()
        raw_data = cls._read_json(config_path)
        cls.app_config = cls._parse_app_config(raw_data)

    # ------------------------------------------------------------------
    # Lectura del archivo
    # ------------------------------------------------------------------

    @classmethod
    def _read_json(cls, path: Path) -> JsonDict:
        if not path.exists():
            raise FileNotFoundError(
                f"Archivo de configuración no encontrado: {path}"
            )
        try:
            with path.open("r", encoding="utf-8") as f:
                data: Any = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"El archivo '{path.name}' no contiene JSON válido."
            ) from exc

        if not isinstance(data, dict):
            raise ValueError(
                f"El archivo '{path.name}' debe contener un objeto JSON en la raíz."
            )

        return data  # type: ignore[return-value]

    # ------------------------------------------------------------------
    # Parseo por secciones
    # ------------------------------------------------------------------

    @classmethod
    def _parse_app_config(cls, data: JsonDict) -> AppConfiguration:
        settings_raw: Any = data.get("settings")

        if not isinstance(settings_raw, dict):
            raise ValueError("La clave 'settings' es obligatoria y debe ser un objeto.")

        settings_data: JsonDict = cast(JsonDict, settings_raw)

        settings = SettingsConfig(
            languages=cls._parse_languages(settings_data),
            csvFile=cls._parse_csv_file(settings_data),
            paths=cls._parse_paths(settings_data),
            keysSheet=cls._parse_keys_sheet(settings_data),
            localePrefixes=cls._parse_locale_prefixes(settings_data),
        )
        
        input_folder_path = Path(settings.paths.inputFolderPath).resolve()
        csv_file_path = (input_folder_path / f"{settings.csvFile.fileName}.csv").resolve();
        
        if input_folder_path not in csv_file_path.parents:
            raise ValueError("La ruta del archivo CSV no es válida.")
        
        cls.input_csv_path = input_folder_path
        cls.input_csv_file_path = csv_file_path        
        
        return AppConfiguration(settings=settings)

    @staticmethod
    def _parse_keys_sheet(settings_data: JsonDict) -> KeysSheetConfiguration:
        keys_sheet_raw: Any = settings_data.get("keysSheet")

        if not isinstance(keys_sheet_raw, dict):
            raise ValueError("'keysSheet' es obligatorio y debe ser un objeto.")

        keys_sheet_data: JsonDict = cast(JsonDict, keys_sheet_raw)

        return KeysSheetConfiguration(
            sheetName=str(keys_sheet_data["sheetName"]),
            generate=bool(keys_sheet_data["generate"]),
            enumName=str(keys_sheet_data["enumName"]),
            enumSummary=str(keys_sheet_data["enumSummary"]),
        )

    @staticmethod
    def _parse_locale_prefixes(settings_data: JsonDict) -> list[PrefixConfiguration]:
        raw_prefixes: Any = settings_data.get("localePrefixes")

        if not isinstance(raw_prefixes, list):
            raise ValueError("'localePrefixes' debe ser una lista.")

        prefixes_data: list[JsonDict] = cast(list[JsonDict], raw_prefixes)
        
        #Comprobamos que cada prefijo esté en mayúsculas y no contenga espacios, para evitar problemas al generar las hojas de idioma y la hoja de claves
        
        for prefix in prefixes_data:
            prefix_value = prefix.get("prefix")
            if not isinstance(prefix_value, str):
                raise ValueError("Cada prefijo debe tener una clave 'prefix' de tipo string.")
            if not prefix_value.isupper():
                raise ValueError(f"El prefijo '{prefix_value}' en la configuración debe estar en mayúsculas.")
            if " " in prefix_value:
                raise ValueError(f"El prefijo '{prefix_value}' no puede contener espacios.")
        
        return [
            PrefixConfiguration(
                prefix=str(prefix["prefix"]),
                regionDescription=str(prefix["regionDescription"]),
            )
            for prefix in prefixes_data
        ]
        
    @staticmethod
    def _parse_languages(settings_data: JsonDict) -> list[LanguageConfiguration]:
        raw_languages: Any = settings_data.get("languages")

        if not isinstance(raw_languages, list):
            raise ValueError("'languages' debe ser una lista.")

        languages_data: list[JsonDict] = cast(list[JsonDict], raw_languages)

        return [
            LanguageConfiguration(
                code=str(lang["code"]),
                fileName=str(lang["fileName"]),
                name=str(lang["name"]),
                summary=str(lang["summary"]),
            )
            for lang in languages_data
        ]

    @staticmethod
    def _parse_csv_file(settings_data: JsonDict) -> CsvFileConfiguration:
        csv_raw: Any = settings_data.get("csvFile")

        if csv_raw is None:
            raise ValueError("'csvFile' es obligatorio.")

        if not isinstance(csv_raw, dict):
            raise ValueError("'csvFile' debe ser un objeto.")

        csv_data: JsonDict = cast(JsonDict, csv_raw)

        return CsvFileConfiguration(
            fileName=str(csv_data["fileName"]),
            columnSeparator=str(csv_data["columnSeparator"]),
            rowSeparator=str(csv_data["rowSeparator"]),
            prefixColumnTag=str(csv_data["prefixColumnTag"]),
            titleColumnTag=str(csv_data["titleColumnTag"]),
            languageColumnTag=str(csv_data["languageColumnTag"]),
        )

    @staticmethod
    def _parse_paths(settings_data: JsonDict) -> PathsConfig:
        paths_raw: Any = settings_data.get("paths")

        if paths_raw is None:
            raise ValueError("'paths' es obligatorio.")


        if not isinstance(paths_raw, dict):
            raise ValueError("'paths' debe ser un objeto.")

        paths_data: JsonDict = cast(JsonDict, paths_raw)

        return PathsConfig(
            outputFolderPath=str(paths_data["outputFolderPath"]),
            inputFolderPath=str(paths_data["inputFolderPath"]),
        )