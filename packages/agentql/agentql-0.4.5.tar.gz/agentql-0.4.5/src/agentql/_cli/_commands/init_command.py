import subprocess
from pathlib import Path

import typer

from agentql.sync_api._agentql_service import check_agentql_server_status, validate_api_key


def _install_dependencies():
    typer.echo("Installing dependencies...")
    try:
        subprocess.run(["playwright", "install", "chromium"], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode().strip()
        typer.echo(
            f"Failed to install dependencies: {error_msg}. If the issue persists, please email support@tinyfish.io",
            err=True,
        )
        raise typer.Exit(code=1)


def _request_api_key():
    typer.echo("For AgentQL API key request, please visit Tiny Fish developer portal.")
    api_key = typer.prompt("Enter your AgentQL API key")
    if not api_key:
        typer.echo("API key cannot be empty.", err=True)
        raise typer.Exit(code=1)
    return api_key


def _check_server_status():
    typer.echo("Checking AgentQL server status...")
    if not check_agentql_server_status():
        typer.echo(
            "AgentQL server is currently unavailable. Please check your internet connection or try again later. If the issue persists, please email support@tinyfish.io",
            err=True,
        )
        raise typer.Exit(code=1)


def _check_api_key(api_key: str):
    typer.echo("Validating AgentQL API key...")
    if not validate_api_key(api_key):
        typer.echo(
            "Invalid AgentQL API key. Please double check the API Key. If the issue persists, please email support@tinyfish.io",
            err=True,
        )
        raise typer.Exit(code=1)


def _save_api_key_to_config_file(api_key: str):
    try:
        typer.echo("Saving AgentQL API key to configuration file...")
        config_file_path = Path.home() / ".agentql" / "config" / "agentql_api_key.ini"
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        config_file_path.write_text(f"[DEFAULT]\nAGENTQL_API_KEY={api_key}\n")
        typer.echo(f"AgentQL API Key saved successfully to {config_file_path}")
    except Exception as e:
        typer.echo(
            f"Failed to write configuration file: {str(e)}. If the issue persists, please email support@tinyfish.io",
            err=True,
        )
        raise typer.Exit(code=1)


def init():
    """Initialize the agentql project."""
    _install_dependencies()
    api_key = _request_api_key()
    _check_server_status()
    _check_api_key(api_key)
    _save_api_key_to_config_file(api_key)
    typer.echo(
        "AgentQL is now ready to use. Follow https://docs.agentql.com/docs/getting-started/first-steps to create your first script."
    )
