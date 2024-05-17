
import os
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

    try:
        os.system(f"cd {destination}\npdm init \npdm add fastapi pydantic pydantic_settings")
 
    
    except Exception:
        typer.echo("PDM is not installed. Please install it and try again.")
        

app.command(name="create")(create)
