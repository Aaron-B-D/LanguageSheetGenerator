from dataclasses import dataclass


@dataclass
class LanguageConfiguration:
    """Representa la configuración de un idioma disponible para traducción."""

    code: str
    """Código identificador del idioma."""

    fileName: str
    """Nombre del archivo asociado al idioma."""

    name: str
    """Nombre descriptivo del idioma."""
    
    summary: str
    """Descripción o resumen del idioma, que se utilizará como comentario en la hoja de idioma"""