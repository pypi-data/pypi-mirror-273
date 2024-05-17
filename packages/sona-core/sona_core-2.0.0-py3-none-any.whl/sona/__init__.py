import typer
from sona.core.commands import app as inferencer_app

app = typer.Typer()
app.add_typer(inferencer_app, name="inferencer")
