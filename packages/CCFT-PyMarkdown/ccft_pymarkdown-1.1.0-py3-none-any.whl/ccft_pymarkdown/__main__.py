"""Command-line execution of the `ccft_pymarkdown` package."""

from collections.abc import Sequence

__all__: Sequence[str] = ()


from ccft_pymarkdown import console

if __name__ == "__main__":
    raise SystemExit(console.run())
