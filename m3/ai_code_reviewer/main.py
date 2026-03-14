"""CLI entry point."""

import sys
import click
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# Dashboard via os.system
from reports.json_reporter import generate_report

@click.group()
def cli():
    pass

@cli.command()
@click.argument("path")
@click.option("--style", default="google")
@click.option("--output", "-o")
def scan(path: str, style: str, output: str):
    """Scan project."""
    report = generate_report(path, output, style)
    click.echo(json.dumps(report, indent=2))

@cli.command()
def dashboard():
    """Run Streamlit dashboard."""
    import os
    os.system("streamlit run ui/dashboard.py")

if __name__ == "__main__":
    cli()

# Fix: run_dashboard not defined; use os.system

