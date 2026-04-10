from pathlib import Path

from src.models.configuration.availablePrefixConfiguration import PrefixConfiguration
from src.models.configuration.languageConfiguration import LanguageConfiguration
from src.models.csv.languageCsv import LanguageCsv
from src.models.languageSheets.languageSheet import LanguageSheet
from src.models.languageSheets.languageSheetEntry import LanguageSheetEntry
from src.models.languageSheets.languageSheetRegion import LanguageSheetRegion


class LanguageSheetUtils:
    """Utilidades relacionadas con la generación de hojas de idiomas."""
    
    available_prefixes: list[PrefixConfiguration] = [];
    """Lista de prefijos disponibles, que se puede actualizar dinámicamente."""
    
    available_prefixes_by_code: dict[str, PrefixConfiguration] = {};
    """Diccionario de prefijos disponibles, indexados por su código para acceso rápido."""
    
    available_languages: list[LanguageConfiguration] = [];
    """Lista de idiomas disponibles, que se puede actualizar dinámicamente."""
    
    available_languages_by_code: dict[str, LanguageConfiguration] = {};
    """Diccionario de idiomas disponibles, indexados por su código para acceso rápido."""
    
    output_folder: Path
    """Ruta de la carpeta de salida para los archivos de hojas de idiomas, que se establece al cargar la configuración principal."""
    
    @staticmethod
    def set_available_prefixes(prefixes: list[PrefixConfiguration]) -> None:
        """Actualiza la lista de prefijos disponibles para los textos en la configuración global."""
        LanguageSheetUtils.available_prefixes = prefixes
        LanguageSheetUtils.available_prefixes_by_code = {prefix.prefix: prefix for prefix in prefixes}
    
    @staticmethod
    def set_available_languages(languages: list[LanguageConfiguration]) -> None:
        """Actualiza la lista de idiomas disponibles para los textos en la configuración global."""
        LanguageSheetUtils.available_languages = languages
        LanguageSheetUtils.available_languages_by_code = {lang.code: lang for lang in languages}
    
    @staticmethod
    def set_output_path_for_language_sheet(output_folder: str) -> None:
        """Establece la ruta de salida para los archivos de hojas de idiomas."""
        LanguageSheetUtils.output_folder = Path(output_folder)
    
    @staticmethod
    def parse_locales_csv_to_language_sheets(csv: LanguageCsv) -> list[LanguageSheet]:
        """Toma el contenido del CSV de idiomas y lo convierte en una lista de objetos LanguageSheet, cada uno representando un idioma con sus regiones y entradas correspondientes."""
        language_sheets: list[LanguageSheet] = []
        
        for language_code in csv.header.languageCodes:
            sheet_title = f"{language_code}"
            available_language = LanguageSheetUtils.available_languages_by_code.get(language_code)
            
            if available_language is None:
                raise ValueError(f"El código de idioma '{language_code}' no está definido en la configuración de idiomas disponibles.")
            else:     
                language_sheet = LanguageSheet(title=sheet_title, regions=[], language_summary=available_language.summary)
                
                for prefix, entries in csv.entriesByPrefix.items():
                    available_prefix = LanguageSheetUtils.available_prefixes_by_code.get(prefix)
                    
                    if available_prefix is None:
                        raise ValueError(f"El prefijo '{prefix}' no está definido en la configuración de prefijos disponibles.")
                    
                    region_description = available_prefix.regionDescription
                    
                    region = LanguageSheetRegion(region_description=region_description, entries=[])
                    
                    language_sheet.addRegion(region)
                    
                    for entry in entries:
                        translation = entry.translations.get(language_code)
                        
                        if translation is None:
                            raise ValueError(f"No se encontró traducción para el idioma '{language_code}' en la entrada con título '{entry.title}' y prefijo '{prefix}'.")
                        
                        region.entries.append(LanguageSheetEntry(key=entry.title, value=translation, prefix=prefix))
                        
                language_sheets.append(language_sheet)
            
        return language_sheets
    
    @staticmethod
    def generate_language_sheet_file(language_sheet: LanguageSheet) -> None:
        LanguageSheetUtils._generate_language_sheet_file(LanguageSheetUtils.output_folder, language_sheet)
    
    @staticmethod
    def _generate_language_sheet_file(output_folder_path: Path, language_sheet: LanguageSheet) -> None:
        """
        Genera un archivo .ts de hoja de idioma en la ruta indicada.
        """
        
        output_path = output_folder_path / f"{language_sheet.title}.ts"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        content = language_sheet.getFormattedSheet()

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(content)
