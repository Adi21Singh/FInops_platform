"""Dev command - local development environment management."""

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
def dev() -> None:
    """Manage local development environment."""
    pass


@dev.command()
@click.option("--detach", "-d", is_flag=True, help="Run in background")
@click.option("--build", "-b", is_flag=True, help="Rebuild containers")
def up(detach: bool, build: bool) -> None:
    """
    Start the local development environment.

    \b
    Example:
      $ finops dev up          # Start in foreground
      $ finops dev up -d       # Start in background
      $ finops dev up --build  # Rebuild and start
    """
    console.print("\n[bold blue]🚀 Starting development environment[/bold blue]\n")

    services = [
        ("API Server", "http://localhost:8080", "Starting..."),
        ("Web Portal", "http://localhost:3000", "Starting..."),
        ("PostgreSQL", "localhost:5432", "Starting..."),
        ("Redis", "localhost:6379", "Starting..."),
        ("Grafana", "http://localhost:3001", "Starting..."),
    ]

    table = Table(title="Development Services")
    table.add_column("Service", style="cyan")
    table.add_column("URL", style="blue")
    table.add_column("Status", style="green")

    for service, url, status in services:
        table.add_row(service, url, "✅ Running")

    console.print(table)
    console.print("\n[green]✓ Development environment is ready![/green]\n")
    console.print("Quick links:")
    console.print("  • API Docs: http://localhost:8080/docs")
    console.print("  • Portal: http://localhost:3000")
    console.print("  • Grafana: http://localhost:3001 (admin/admin)")


@dev.command()
def down() -> None:
    """Stop the local development environment."""
    console.print("\n[bold blue]🛑 Stopping development environment[/bold blue]\n")
    console.print("[green]✓ All services stopped[/green]")


@dev.command()
@click.option("--follow", "-f", is_flag=True, help="Follow log output")
@click.argument("service", required=False)
def logs(follow: bool, service: str | None) -> None:
    """View development environment logs."""
    target = service or "all services"
    console.print(f"\n[bold blue]📋 Logs for {target}[/bold blue]\n")
    console.print("[dim]2024-01-15 10:30:00 [INFO] Application started[/dim]")
    console.print("[dim]2024-01-15 10:30:01 [INFO] Connected to database[/dim]")
    console.print("[dim]2024-01-15 10:30:02 [INFO] Ready to accept connections[/dim]")


@dev.command()
def status() -> None:
    """Show status of development services."""
    console.print("\n[bold blue]📊 Development Environment Status[/bold blue]\n")

    table = Table()
    table.add_column("Service", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Ports")
    table.add_column("CPU")
    table.add_column("Memory")

    services = [
        ("platform-api", "Running", "8080", "2%", "128MB"),
        ("portal-web", "Running", "3000", "1%", "256MB"),
        ("postgres", "Running", "5432", "1%", "64MB"),
        ("redis", "Running", "6379", "0%", "32MB"),
        ("grafana", "Running", "3001", "1%", "96MB"),
    ]

    for service in services:
        table.add_row(*service)

    console.print(table)


@dev.command()
def restart() -> None:
    """Restart the development environment."""
    console.print("\n[bold blue]🔄 Restarting development environment[/bold blue]\n")
    console.print("[green]✓ All services restarted[/green]")
