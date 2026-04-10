## Utils responsable de la gestión del archivo CSV empleado para generar las hojas de idiomas

from pathlib import Path

from src.models.configuration.availablePrefixConfiguration import PrefixConfiguration
from src.models.configuration.csvFileConfiguration import CsvFileConfiguration
from src.models.configuration.languageConfiguration import LanguageConfiguration
from src.models.csv.languageCsv import LanguageCsv
from src.models.csv.languageCsvEntry import LanguageCsvEntry
from src.models.csv.languageCsvHeader import LanguageCsvHeader


class LocalesCsvUtils:
    """Utilidades para la gestión del archivo CSV de entrada."""
    
    configuration: CsvFileConfiguration | None = None;
    """Configuración global del CSV, que se establece al cargar la configuración principal."""
    
    localePrefixes: list[str] = [];
    """Lista de prefijos disponibles, que se puede actualizar dinámicamente."""
    
    availableLanguages: list[LanguageConfiguration] = [];
    """Lista de idiomas disponibles, que se puede actualizar dinámicamente."""
    
    @staticmethod
    def set_csv_config(csv_config: CsvFileConfiguration) -> None:
        """Toma los parámetros de configuración del CSV y los aplica a la configuración global."""
        LocalesCsvUtils.configuration = csv_config;
        
        
    @staticmethod
    def set_available_prefixes(prefixes: list[PrefixConfiguration]) -> None:
        """Actualiza la lista de prefijos disponibles para los textos en la configuración global."""
        if LocalesCsvUtils.configuration is None:
            raise ValueError("La configuración del CSV no se ha establecido.")
            
        LocalesCsvUtils.localePrefixes = [prefix.prefix for prefix in prefixes]
        
    @staticmethod
    def set_available_languages(languages: list[LanguageConfiguration]) -> None:
        """Actualiza la lista de idiomas disponibles para los textos en la configuración global."""
        if LocalesCsvUtils.configuration is None:
            raise ValueError("La configuración del CSV no se ha establecido.")
            
        LocalesCsvUtils.availableLanguages = languages
        
    @staticmethod
    def get_csv_file_content(path: Path) -> str:
        """Lee el contenido del archivo CSV ubicado en la ruta especificada."""
        if not path.is_file():
            raise FileNotFoundError(f"El archivo CSV no se encontró en la ruta: {path}")
        
        return path.read_text(encoding="utf-8")
    
    @staticmethod
    def parse_language_csv_header(header_line: str) -> LanguageCsvHeader:
        """Parsea la línea de encabezado del CSV y devuelve una instancia de LanguageCsvHeader."""
        if LocalesCsvUtils.configuration is None:
            raise ValueError("La configuración del CSV no se ha establecido.")
        
        column_separator = LocalesCsvUtils.configuration.columnSeparator
        columns = [column.strip() for column in header_line.split(column_separator)]

        prefix_column_tag = LocalesCsvUtils.configuration.prefixColumnTag
        title_column_tag = LocalesCsvUtils.configuration.titleColumnTag
        language_column_tag = LocalesCsvUtils.configuration.languageColumnTag;
        
        prefix_column_index = -1
        title_column_index = -1
        language_columns: dict[str, int] = {}

        for index, column in enumerate(columns):
            if column.startswith(f"[{prefix_column_tag}]"):
                prefix_column_index = index
                continue
            elif column.startswith(f"[{title_column_tag}]"):
                title_column_index = index
                continue

            elif column.startswith(f"[{language_column_tag}]"):
                language_code = column.removeprefix(f"[{language_column_tag}]").strip()

                if not language_code:
                    raise ValueError(
                        f"La columna de idioma en posición {index} no tiene código de idioma."
                    )
                    
                if language_code in language_columns:
                    raise ValueError(
                        f"Código de idioma duplicado en el encabezado: '{language_code}' en posición {index}."
                    )
                
                available_language_codes = [lang.code for lang in LocalesCsvUtils.availableLanguages]
                if language_code not in available_language_codes:
                    raise ValueError(
                        f"Código de idioma no reconocido en el encabezado: '{language_code}' en posición {index}."
                    )
                
                language_columns[language_code] = index
            else:
                raise ValueError(
                    f"Columna no reconocida en el encabezado: '{column}' en posición {index}."
                )

        if prefix_column_index == -1:
            raise ValueError(F"No se encontró la columna de prefijo ([{prefix_column_tag}]).")

        if title_column_index == -1:
            raise ValueError(f"No se encontró la columna de título ([{title_column_tag}]).")

        if not language_columns:
            raise ValueError(f"No se encontró ninguna columna de idioma ([{language_column_tag}]).")

        return LanguageCsvHeader(
            prefixColumnName=columns[prefix_column_index],
            prefixColumnPosition=prefix_column_index,
            titleColumnName=columns[title_column_index],
            titleColumnPosition=title_column_index,
            languageCodes=language_columns
        )

    @staticmethod
    def parse_language_csv_entry(line: str, header: LanguageCsvHeader) -> LanguageCsvEntry:
        """Parsea una línea del CSV (que representa una entrada) y devuelve una instancia de LanguageCsvEntry."""
        if LocalesCsvUtils.configuration is None:
            raise ValueError("La configuración del CSV no se ha establecido.")
        
        column_separator = LocalesCsvUtils.configuration.columnSeparator
        columns = [column.strip() for column in line.split(column_separator)]

        prefix = columns[header.prefixColumnPosition]
        title = columns[header.titleColumnPosition]

        translations: dict[str, str] = {}
        for language_code, position in header.languageCodes.items():
            translations[language_code] = columns[position]

        result = LanguageCsvEntry(
            prefix=prefix,
            title=title,
            translations=translations
        )
        
        ## Validaciones varias para asegurar que los datos cumplen con los requisitos esperados, como que el prefijo y la clave/título no estén vacíos, estén en mayúsculas y no contengan espacios, y que las traducciones no estén vacías.
        if not result.prefix:
            raise ValueError(f"El prefijo no puede estar vacío en la línea: '{line}'.")
        if not result.prefix.isupper():
            raise ValueError(f"El prefijo debe estar en mayúsculas en la línea: '{line}'.")
        if " " in result.prefix:
            raise ValueError(f"El prefijo no puede contener espacios en la línea: '{line}'.")
        if result.title == "":
            raise ValueError(f"La clave/título no puede estar vacío en la línea: '{line}'.")
        if not result.title.isupper():
            raise ValueError(f"La clave/título debe estar en mayúsculas en la línea: '{line}'.")
        if " " in result.title:
            raise ValueError(f"La clave/título no puede contener espacios en la línea: '{line}'.")        

        for language_code, translation in result.translations.items():
            if translation == "":
                raise ValueError(f"La traducción para el idioma '{language_code}' no puede estar vacía en la línea: '{line}'.")
        
        return result
    
    @staticmethod
    def parse_language_csv(content: str) -> LanguageCsv:
        """Parsea el contenido del CSV de idiomas y devuelve una instancia de LanguageCsv."""
        if LocalesCsvUtils.configuration is None:
            raise ValueError("La configuración del CSV no se ha establecido.")
        
        lineSeparator = LocalesCsvUtils.configuration.rowSeparator
        
        lines = [line.strip() for line in content.split(lineSeparator) if line.strip()]
        if not lines:
            raise ValueError("El archivo CSV está vacío.")
        
        header_line = lines[0]
        header = LocalesCsvUtils.parse_language_csv_header(header_line)
        entries: list[LanguageCsvEntry] = []
        for line in lines[1:]:
            entry = LocalesCsvUtils.parse_language_csv_entry(line, header)
            entries.append(entry)
            
        if not entries:
            raise ValueError("El archivo CSV no contiene ninguna entrada de idioma.")
        
        for entry in entries:
            if entry.getFullName() in [e.getFullName() for e in entries if e != entry]:
                raise ValueError(f"Entrada duplicada encontrada: '{entry.getFullName()}'. Cada combinación de prefijo y título debe ser única.")
        
        return LanguageCsv(
            content=content,
            header=header,
            entries=entries
        )
        