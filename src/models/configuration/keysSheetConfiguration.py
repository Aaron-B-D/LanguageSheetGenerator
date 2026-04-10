class KeysSheetConfiguration:
    """Representa la configuración específica para la hoja de claves (keys sheet)"""
    
    def __init__(self, sheetName: str, generate: bool, enumName: str, enumSummary: str) -> None:
        self.sheetName = sheetName
        """Nombre de la hoja que se generará para las claves."""
        self.generate = generate
        """Indica si se debe generar la hoja de claves o no."""
        self.enumName = enumName
        """Nombre del enum que se generará en la hoja de claves, si se ha habilitado su generación."""
        self.summary = enumSummary
        """Descripción o resumen del enum que se generará en la hoja de claves, que se utilizará como comentario en el archivo generado."""