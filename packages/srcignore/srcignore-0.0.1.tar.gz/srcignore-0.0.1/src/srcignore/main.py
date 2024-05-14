#
#  Copyright 2024 Calian Ltd. All rights reserved.
#


from pathlib import Path

import typer
from gitignore_parser import parse_gitignore
from typing_extensions import Annotated, List

app = typer.Typer()

def hi():
    print(hi)

@app.command()
def ls(
    projectroot: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    ignore_files: Annotated[
        List[Path],
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
):
    matches = [ parse_gitignore(file) for file in ignore_files ]

    for filename in projectroot.rglob("*"):
        for match in matches:
            if match(filename):
                print(filename.relative_to(projectroot))
                break


if __name__ == "__main__":  # pragma: no cover
    app()
