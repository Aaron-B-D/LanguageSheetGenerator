from pathlib import Path

from src.models.configuration.keysSheetConfiguration import KeysSheetConfiguration
from src.models.csv.languageCsvEntry import LanguageCsvEntry


class KeysSheetUtils:
    """Utilidades para la generación de la hoja de claves (keys sheet)"""
    
    output_folder_path: Path;
    config: KeysSheetConfiguration;
    
    @staticmethod
    def set_output_path_for_language_sheet(output_folder_path: str) -> None:
        """Configura la ruta de salida para la hoja de claves."""
        KeysSheetUtils.output_folder_path = Path(output_folder_path).resolve()
        
    @staticmethod
    def set_config(keys_sheet_config: KeysSheetConfiguration) -> None:
        """Configura los parámetros específicos para la hoja de claves."""
        config = keys_sheet_config
        KeysSheetUtils.config = config
        
    @staticmethod
    def generate_keys_sheet(csv_entries: list[LanguageCsvEntry]) -> None:
        """Genera la hoja de claves con las entradas proporcionadas. Lo generará como un enumerado de Typescript con cada valor siendo la key en string"""
        
        if not KeysSheetUtils.config.generate:
            print("La generación de la hoja de claves está deshabilitada en la configuración. No se generará el archivo de claves.")
        else:
            output_path = KeysSheetUtils.output_folder_path / f"{KeysSheetUtils.config.sheetName}.ts"
            
            with output_path.open("w", encoding="utf-8") as f:
                f.write(f"/** {KeysSheetUtils.config.summary} */\nexport enum {KeysSheetUtils.config.enumName} {{\n")
                for entry in csv_entries:
                    key_name = entry.getFullName()
                    f.write(f"\t{key_name} = \"{key_name}\",\n")
                f.write("}")