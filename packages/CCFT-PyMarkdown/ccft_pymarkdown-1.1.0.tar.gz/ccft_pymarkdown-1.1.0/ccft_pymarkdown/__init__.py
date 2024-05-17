"""A Python helper script to load a set of mods from a local mods-list."""

from collections.abc import Sequence

__all__: Sequence[str] = (
    "run",
    "restore_all_markdown_files",
    "clean_custom_formatted_tables_from_all_files",
    "clean_custom_formatted_tables_from_single_file",
    "CleanCustomFormattedTables",
)
__version__ = "v1.1.0"


from ccft_pymarkdown.clean_custom_formatted_tables import (
    clean_custom_formatted_tables_from_all_files,
    clean_custom_formatted_tables_from_single_file,
)
from ccft_pymarkdown.console import run
from ccft_pymarkdown.context_manager import CleanCustomFormattedTables
from ccft_pymarkdown.restore_files import (
    restore_all_markdown_files,
)
