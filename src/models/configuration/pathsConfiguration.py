from dataclasses import dataclass


@dataclass
class PathsConfig:
    """Define las rutas de entrada y salida del proceso."""

    outputFolderPath: str
    """Ruta de la carpeta donde se generarán los archivos de salida."""

    inputFolderPath: str
    """Ruta de la carpeta que contiene los archivos fuente."""
