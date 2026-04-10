## La clase que representa el CSV de idiomas

from src.models.csv.languageCsvEntry import LanguageCsvEntry
from src.models.csv.languageCsvHeader import LanguageCsvHeader


class LanguageCsv:
    """Representa el archivo CSV de idiomas, con su contenido y configuración."""
    
    content: str
    """Contenido completo del archivo CSV, leído como texto."""
    
    header: LanguageCsvHeader;
    """Encabezado del CSV, con los nombres de las columnas y códigos de idioma."""
    
    entries: list[LanguageCsvEntry];
    """Lista de entradas del CSV, cada una representando una fila con su clave y traducciones."""
      
    entriesByPrefix: dict[str, list[LanguageCsvEntry]];
    """Diccionario que mapea cada prefijo a la lista de entradas que lo contienen, para facilitar el filtrado por prefijo."""
      
    def __init__(self, content: str, header: LanguageCsvHeader, entries: list[LanguageCsvEntry]) -> None:
        self.content = content
        self.header = header
        self.entries = entries
        self.entriesByPrefix = {}
        for entry in entries:
            prefix = entry.prefix
            if prefix not in self.entriesByPrefix:
                self.entriesByPrefix[prefix] = []
            self.entriesByPrefix[prefix].append(entry)