## Clase que representa la fila de encabezado del CSV de idiomas

class LanguageCsvHeader:
    """Representa la fila de encabezado del CSV de idiomas, con los nombres de las columnas."""
    
    prefixColumnName: str
    """Nombre de la columna que contiene el prefijo."""
    
    prefixColumnPosition: int
    """Posición (índice) de la columna que contiene el prefijo."""
    
    titleColumnName: str
    """Nombre de la columna que contiene la clave o título."""
    
    titleColumnPosition: int
    """Posición (índice) de la columna que contiene la clave o título."""
    
    languageCodes: dict[str, int]
    """Diccionario de códigos de idioma presentes en el encabezado, indicando las columnas de traducción."""
    
    
    def __init__(self, prefixColumnName: str, prefixColumnPosition: int, titleColumnName: str, titleColumnPosition: int, languageCodes: dict[str, int]) -> None:
        self.prefixColumnName = prefixColumnName
        self.prefixColumnPosition = prefixColumnPosition
        self.titleColumnName = titleColumnName
        self.titleColumnPosition = titleColumnPosition
        self.languageCodes = languageCodes