
from pathlib import Path
import typer
import shutil
from addecli.create import create

app = typer.Typer()


@app.command(name="init")
def init(destination: str):
    source = Path(__file__).parent / "init_project"
    shutil.copytree(source, f"./{destination}")
    typer.echo(f"Folder copied from {source} to {destination}")

app.command(name="create")(create)
