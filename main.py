from typing import Optional


from src.models.configuration.appConfiguration import AppConfiguration
from src.models.csv.languageCsv import LanguageCsv
from src.utils.configurationUtils import ConfigurationUtils
from src.utils.keysSheetUtils import KeysSheetUtils
from src.utils.languageSheetUtils import LanguageSheetUtils
from src.utils.localesCsvUtils import LocalesCsvUtils

app_settings: Optional[AppConfiguration] = None

def main() -> None:
    """Función principal que carga la configuración, procesa el archivo CSV de entrada y genera las hojas de idioma y la hoja de claves según la configuración."""
    loadAppConfiguration();
    if app_settings is None:
        raise ValueError("La configuración de la aplicación no se ha cargado correctamente.")
    else:
        initialize(app_settings)
        generate()
    
def initialize(app_settings: AppConfiguration) -> None:
    """Inicializa las utilidades y configuraciones necesarias para la generación de las hojas de idioma y la hoja de claves."""
    LocalesCsvUtils.set_csv_config(app_settings.settings.csvFile);
    LocalesCsvUtils.set_available_prefixes(app_settings.settings.localePrefixes);
    LocalesCsvUtils.set_available_languages(app_settings.settings.languages);
    LanguageSheetUtils.set_available_prefixes(app_settings.settings.localePrefixes);
    LanguageSheetUtils.set_available_languages(app_settings.settings.languages);
    LanguageSheetUtils.set_output_path_for_language_sheet(app_settings.settings.paths.outputFolderPath);
    KeysSheetUtils.set_config(app_settings.settings.keysSheet);
    KeysSheetUtils.set_output_path_for_language_sheet(app_settings.settings.paths.outputFolderPath);
        
def loadAppConfiguration() -> None:
    """Carga la configuración principal de la aplicación desde el archivo de configuración y la almacena en una variable global."""
    ConfigurationUtils.load_configuration();
    global app_settings
    app_settings = ConfigurationUtils.app_config;
    
def generate()-> None:
    """Genera las hojas de idioma y la hoja de claves a partir del archivo CSV de entrada y la configuración cargada."""
    csv: LanguageCsv = LocalesCsvUtils.parse_language_csv(LocalesCsvUtils.get_csv_file_content(ConfigurationUtils.input_csv_file_path))
    languageSheets = LanguageSheetUtils.parse_locales_csv_to_language_sheets(csv)

    for sheet in languageSheets:
        LanguageSheetUtils.generate_language_sheet_file(sheet)
    
    KeysSheetUtils.generate_keys_sheet(csv.entries)

success = False;        
try:
    main()
    success = True

except Exception as exc:
    print(f"Error: {exc}")
if success:
    if(app_settings is not None and app_settings.settings.keysSheet.generate):
        print("Hojas de idioma y hoja de claves generadas exitosamente.")
    else:
        print("Hojas de idioma generadas exitosamente.")
else:
    print("No se pudieron generar las hojas de idioma.")
input("Presiona Enter para salir...")