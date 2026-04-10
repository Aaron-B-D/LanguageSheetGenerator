from src.models.languageSheets.languageSheetRegion import LanguageSheetRegion


class LanguageSheet:
    """Representa una hoja de idioma con su título, idioma y prefijo."""
    
    
    def __init__(self, title: str, regions: list[LanguageSheetRegion], language_summary: str):
        self.title = title
        """ El título de la hoja de idioma, que se utilizará como nombre del archivo de salida. """
        self.regions: list[LanguageSheetRegion] = regions
        """ Lista de regiones dentro de la hoja, cada una con su descripción y entradas asociadas. """
        self.language_summary = language_summary
        """ Descripción del idioma representado por la hoja. """
        
    def addRegion(self, region: LanguageSheetRegion) -> None:
        """Agrega una región a la hoja de idioma."""
        self.regions.append(region)
        
    def getFormattedSheet(self) -> str:
        """Devuelve la hoja de idioma formateada como un bloque de TypeScript, con todas sus regiones y entradas ordenadas alfabéticamente."""
        
        sorted_regions = sorted(
            self.regions,
            key=lambda region: region.regionDescription.upper()
        )
        
        formatted_regions = "\n\n\n\n".join(
            region.getFormattedRegion(indentation_level=1)
            for region in sorted_regions
        )
        
        if self.language_summary.strip() == "":
            self.language_summary = f" {self.language_summary.strip()} "
            return (
                f"export const {self.title} = {{\n"
                f"{formatted_regions}\n"
                f"}};"
            )
        else:       
            return (
                f"/** {self.language_summary} */\nexport const {self.title} = {{\n"
                f"{formatted_regions}\n"
                f"}};"
            )