## Representa una fila del CSV de idiomas, con su clave y traducciones

class LanguageCsvEntry:
    """Representa una fila del CSV de idiomas, con su clave y traducciones."""
    
    prefix: str
    """Prefijo asociado a la entrada, para filtrado o categorización."""
    
    title: str
    """Clave o título que identifica el texto a traducir."""
    
    translations: dict[str, str]
    """Diccionario que mapea códigos de idioma a sus traducciones correspondientes."""
    
    def __init__(self, prefix: str, title: str, translations: dict[str, str]) -> None:
        self.prefix = prefix
        self.title = title
        self.translations = translations
        
    def getFullName(self) -> str:
        """Devuelve el nombre completo de la entrada, combinando el prefijo y el título."""
        return f"{self.prefix}_{self.title}"