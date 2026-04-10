class LanguageSheetEntry:
    """Representa una entrada dentro de una hoja de idioma, con su clave, valor y prefijo."""
    
    def __init__(self, key: str, value: str, prefix: str):
        self.key = key
        """ La clave o título que identifica el texto a traducir. """
        self.value = value
        """ El valor traducido correspondiente a la clave. """
        self.prefix = prefix
        
    def getFormattedLine(self) -> str:
        """Devuelve la entrada formateada como una propiedadde un objeto TypeScript."""

        return f"{self.prefix.upper()}_{self.key.upper()}: '{self.value}',"