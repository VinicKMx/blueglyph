"""Typer command-line entry point."""

from __future__ import annotations

import typer
from rich.console import Console

from bledev import __version__
from bledev.api import new_capture_session
from bledev.protocol.usb import HEADER_SIZE, PROTOCOL_MAGIC, PROTOCOL_VERSION

app = typer.Typer(
    add_completion=False,
    help="BLE debugger and sniffer tooling for nRF52840 capture hardware.",
)
console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", help="Show the host package version."),
) -> None:
    """Run bledev."""

    if version:
        console.print(__version__)
        raise typer.Exit
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
        raise typer.Exit


@app.command()
def status() -> None:
    """Show host readiness and current transport state."""

    session = new_capture_session()
    console.print("[bold]Host[/bold]")
    console.print(f"Version: {session.metadata.host_version}")
    console.print("Transport: not connected")
    console.print("Capture: idle")


@app.command("protocol-info")
def protocol_info() -> None:
    """Show the currently supported USB protocol framing version."""

    console.print("[bold]USB protocol[/bold]")
    console.print(f"Version: {PROTOCOL_VERSION}")
    console.print(f"Magic: 0x{PROTOCOL_MAGIC:04X}")
    console.print(f"Header size: {HEADER_SIZE} bytes")
