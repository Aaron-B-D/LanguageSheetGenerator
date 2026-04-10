from dataclasses import dataclass


@dataclass
class PrefixConfiguration:
    """Representa la configuración de un prefijo disponible"""
    
    prefix: str
    regionDescription: str

    def __init__(self, prefix: str, regionDescription: str):
        self.prefix = prefix
        """ El prefijo en sí, que se utilizará para identificar las entradas que pertenecen a esta categoría. """
        self.regionDescription = regionDescription
        """ La descripción de la región, que se utilizará como comentario en la hoja de idioma para identificar visualmente las entradas que pertenecen a esta categoría. """
        