"""
Streamviz CLI - Streamlit-like interface for dashboard development.

Usage:
    streamviz serve dashboard.py
    streamviz validate dashboard.py
    streamviz list
"""

import importlib.util
import sys
import time
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from viz.api.registry import RegistryClient
from viz.layout.dashboard import Dashboard

console = Console()


class DashboardFileHandler(FileSystemEventHandler):
    """File watcher handler for dashboard file changes."""

    def __init__(self, filepath: Path, callback):
        self.filepath = filepath.resolve()
        self.callback = callback
        self.last_modified = 0

    def on_modified(self, event):
        """Handle file modification events."""
        if event.src_path == str(self.filepath):
            # Debounce rapid file changes
            current_time = time.time()
            if current_time - self.last_modified > 1.0:
                self.last_modified = current_time
                self.callback()


def load_dashboard_from_file(filepath: Path) -> Optional[Dashboard]:
    """
    Load a dashboard from a Python file.

    Args:
        filepath: Path to dashboard file

    Returns:
        Dashboard instance or None if loading fails
    """
    try:
        # Load module from file
        spec = importlib.util.spec_from_file_location("dashboard_module", filepath)
        if not spec or not spec.loader:
            console.print(f"[red]✗[/red] Could not load file: {filepath}")
            return None

        module = importlib.util.module_from_spec(spec)
        sys.modules["dashboard_module"] = module
        spec.loader.exec_module(module)

        # Find Dashboard instance in module
        dashboard = None
        for name, obj in vars(module).items():
            if isinstance(obj, Dashboard):
                dashboard = obj
                break

        if not dashboard:
            console.print("[red]✗[/red] No Dashboard instance found in file")
            console.print("[yellow]Hint:[/yellow] Make sure you create a Dashboard object in your file")
            return None

        return dashboard

    except Exception as e:
        console.print(f"[red]✗[/red] Error loading dashboard: {e}")
        import traceback
        console.print(traceback.format_exc())
        return None


def validate_dashboard(dashboard: Dashboard) -> bool:
    """
    Validate a dashboard structure.

    Args:
        dashboard: Dashboard instance

    Returns:
        True if valid, False otherwise
    """
    errors = []
    warnings = []

    # Check basic structure
    if not dashboard.title:
        errors.append("Dashboard must have a title")

    if not dashboard.children:
        errors.append("Dashboard must have at least one page")

    # Check for duplicate IDs
    seen_ids = set()
    def check_ids(node, path=""):
        if hasattr(node, 'id') and node.id:
            if node.id in seen_ids:
                errors.append(f"Duplicate ID '{node.id}' at {path}")
            seen_ids.add(node.id)

        if hasattr(node, 'children'):
            for i, child in enumerate(node.children):
                check_ids(child, f"{path}/{type(node).__name__}[{i}]")

    check_ids(dashboard)

    # Display results
    if errors:
        console.print("\n[red]Validation Errors:[/red]")
        for error in errors:
            console.print(f"  [red]✗[/red] {error}")

    if warnings:
        console.print("\n[yellow]Warnings:[/yellow]")
        for warning in warnings:
            console.print(f"  [yellow]⚠[/yellow] {warning}")

    if not errors and not warnings:
        console.print("[green]✓[/green] Dashboard structure is valid")
        return True
    elif not errors:
        console.print(f"\n[yellow]Validation passed with {len(warnings)} warning(s)[/yellow]")
        return True
    else:
        console.print(f"\n[red]Validation failed with {len(errors)} error(s)[/red]")
        return False


@click.group()
@click.version_option(version="0.1.0", prog_name="streamviz")
def cli():
    """Streamviz - Distributed dashboarding framework CLI."""
    pass


@cli.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--registry-url', default='http://localhost:8000', help='Registry API URL')
@click.option('--username', envvar='VIZ_USERNAME', help='Registry username')
@click.option('--password', envvar='VIZ_PASSWORD', help='Registry password')
@click.option('--watch/--no-watch', default=True, help='Watch file for changes')
@click.option('--validate/--no-validate', default=True, help='Validate before registering')
def serve(filepath: str, registry_url: str, username: Optional[str], password: Optional[str], watch: bool, validate: bool):
    """
    Serve a dashboard file with auto-reload.

    Example:
        streamviz serve examples/sales_dashboard.py
    """
    filepath = Path(filepath).resolve()

    if not username or not password:
        console.print("[red]✗[/red] Authentication required")
        console.print("Set VIZ_USERNAME and VIZ_PASSWORD environment variables")
        console.print("Or use --username and --password options")
        sys.exit(1)

    # Show header
    console.print(Panel.fit(
        f"[bold cyan]Streamviz Dashboard Server[/bold cyan]\n"
        f"File: {filepath}\n"
        f"Registry: {registry_url}",
        border_style="cyan"
    ))

    # Initial registration
    def register_dashboard():
        console.print(f"\n[cyan]Loading dashboard from {filepath.name}...[/cyan]")

        # Load dashboard
        dashboard = load_dashboard_from_file(filepath)
        if not dashboard:
            return

        # Validate
        if validate:
            console.print("\n[cyan]Validating dashboard...[/cyan]")
            if not validate_dashboard(dashboard):
                console.print("[yellow]⚠[/yellow] Continuing despite validation errors...")

        # Register with registry
        try:
            console.print(f"\n[cyan]Connecting to registry at {registry_url}...[/cyan]")
            with RegistryClient(base_url=registry_url, username=username, password=password) as client:
                console.print("[green]✓[/green] Authenticated\n")
                results = client.register_dashboard_full(dashboard)

                # Summary
                console.print("\n" + "="*60)
                console.print("[bold green]Registration Complete[/bold green]")
                console.print(f"  Functions: {len(results['functions'])}")
                console.print(f"  Components: {len(results['components'])}")
                console.print(f"  Dashboard: {dashboard.id}")
                if results['errors']:
                    console.print(f"  [red]Errors: {len(results['errors'])}[/red]")
                console.print("="*60)

        except Exception as e:
            console.print(f"\n[red]✗[/red] Registration failed: {e}")
            import traceback
            console.print(traceback.format_exc())

    # Do initial registration
    register_dashboard()

    # Watch for changes
    if watch:
        console.print(f"\n[cyan]Watching for changes...[/cyan] (Press Ctrl+C to stop)")

        handler = DashboardFileHandler(filepath, register_dashboard)
        observer = Observer()
        observer.schedule(handler, str(filepath.parent), recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            console.print("\n[yellow]Stopping file watcher...[/yellow]")
            observer.stop()
        observer.join()

    else:
        console.print("\n[cyan]File watching disabled. Dashboard registered once.[/cyan]")


@cli.command()
@click.argument('filepath', type=click.Path(exists=True))
def validate(filepath: str):
    """
    Validate a dashboard file without registering.

    Example:
        streamviz validate examples/sales_dashboard.py
    """
    filepath = Path(filepath).resolve()

    console.print(f"[cyan]Validating {filepath.name}...[/cyan]\n")

    # Load dashboard
    dashboard = load_dashboard_from_file(filepath)
    if not dashboard:
        sys.exit(1)

    # Validate
    is_valid = validate_dashboard(dashboard)
    sys.exit(0 if is_valid else 1)


@cli.command()
@click.option('--registry-url', default='http://localhost:8000', help='Registry API URL')
@click.option('--username', envvar='VIZ_USERNAME', help='Registry username')
@click.option('--password', envvar='VIZ_PASSWORD', help='Registry password')
def list(registry_url: str, username: Optional[str], password: Optional[str]):
    """
    List registered dashboards.

    Example:
        streamviz list
    """
    if not username or not password:
        console.print("[red]✗[/red] Authentication required")
        sys.exit(1)

    try:
        with RegistryClient(base_url=registry_url, username=username, password=password) as client:
            response = client.client.get(
                f"{registry_url}/dashboards/",
                headers=client._get_headers()
            )
            response.raise_for_status()
            dashboards = response.json()

            if not dashboards:
                console.print("[yellow]No dashboards registered[/yellow]")
                return

            console.print(f"\n[bold]Registered Dashboards:[/bold]\n")
            for db in dashboards:
                console.print(f"  [cyan]•[/cyan] {db['id']} - {db['title']}")
                console.print(f"    URL: {registry_url}/dashboards/{db['id']}")
                console.print(f"    Updated: {db['updated_at']}\n")

    except Exception as e:
        console.print(f"[red]✗[/red] Failed to list dashboards: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
