from dataclasses import dataclass


@dataclass
class CsvFileConfiguration:
    """Contiene la configuración del archivo CSV de entrada."""

    fileName: str
    """Nombre del archivo CSV que contiene los textos."""

    columnSeparator: str
    """Carácter utilizado para separar columnas."""

    rowSeparator: str
    """Carácter o secuencia usada para separar filas."""

    prefixColumnTag: str
    """Etiqueta de la columna que contiene el prefijo. Deberá ir entre corches. Por ejemplo [PREFIX]"""

    titleColumnTag: str
    """Etiqueta de la columna que contiene la clave o título. Deberá ir entre corches. Por ejemplo [TITLE]"""
    
    languageColumnTag: str
    """Etiqueta común para marcar las columnas de traducción. Deberá ir entre corches. Por ejemplo [LANG]es_ES"""
