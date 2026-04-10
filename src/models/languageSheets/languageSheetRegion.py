from src.models.languageSheets.languageSheetEntry import LanguageSheetEntry


class LanguageSheetRegion:
    """Representa una región de traducciones dentro de una hoja de idioma."""

    def __init__(self, region_description: str, entries: list[LanguageSheetEntry]):
        self.regionDescription = region_description
        self.entries: list[LanguageSheetEntry] = entries

    def add_entry(self, entry: LanguageSheetEntry) -> None:
        """Añade una entrada a la región."""
        self.entries.append(entry)

    def getFormattedRegion(self, indentation_level: int = 1) -> str:
        """
        Devuelve la región formateada como un bloque de TypeScript,
        ordenando las entradas alfabéticamente por clave.
        """

        indentation = "\t" * indentation_level

        sorted_entries = sorted(
            self.entries,
            key=lambda entry: entry.key.upper()
        )

        formatted_entries = "\n".join(
            f"{indentation}{entry.getFormattedLine()}"
            for entry in sorted_entries
        )

        return (
            f"{indentation}//#region {self.regionDescription}\n\n"
            f"{formatted_entries}\n\n"
            f"{indentation}//#endregion {self.regionDescription}"
        )