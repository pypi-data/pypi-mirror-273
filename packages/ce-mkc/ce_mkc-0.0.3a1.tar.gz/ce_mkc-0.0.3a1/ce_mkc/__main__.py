"""MKC entry point script."""
# ce_mkc/__main__.py

from ce_mkc.main.ce_mkc import main

from .cli.cli import run

if __name__ == "__main__":
    run()

