"""Custom context manager to clean custom-formatted tables only inside the context."""

from collections.abc import Sequence

__all__: Sequence[str] = ("CleanCustomFormattedTables",)


from types import TracebackType

from ccft_pymarkdown import (
    clean_custom_formatted_tables,
    restore_files,
)


class CleanCustomFormattedTables:
    """Context manager to clean custom-formatted tables only inside the context."""

    def __enter__(self) -> None:
        """Clean custom-formatted tables before entering the context."""
        clean_custom_formatted_tables.clean_custom_formatted_tables_from_all_files()

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:  # noqa: E501
        """Restore Markdown files back to their original state."""
        restore_files.restore_all_markdown_files()
