"""Services command - manage platform services."""

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
def services() -> None:
    """Manage platform services."""
    pass


@services.command("list")
@click.option("--team", "-t", help="Filter by team")
@click.option("--env", "-e", help="Filter by environment")
def list_services(team: str | None, env: str | None) -> None:
    """
    List all services in the platform.

    \b
    Example:
      $ finops services list
      $ finops services list --team backend
      $ finops services list --env prod
    """
    console.print("\n[bold blue]📋 Platform Services[/bold blue]\n")

    table = Table()
    table.add_column("Name", style="cyan")
    table.add_column("Team", style="magenta")
    table.add_column("Template")
    table.add_column("Dev", justify="center")
    table.add_column("Staging", justify="center")
    table.add_column("Prod", justify="center")
    table.add_column("Last Deploy")

    # Sample services
    services_data = [
        ("trading-api", "backend", "python-microservice", "✅", "✅", "✅", "2h ago"),
        ("user-service", "platform", "python-microservice", "✅", "✅", "✅", "1d ago"),
        ("payment-processor", "payments", "event-processor", "✅", "✅", "⏸️", "3d ago"),
        ("analytics-etl", "data", "batch-job", "✅", "✅", "✅", "6h ago"),
        ("notification-svc", "platform", "node-microservice", "✅", "🔄", "⏸️", "5m ago"),
    ]

    for svc in services_data:
        if team and svc[1] != team:
            continue
        table.add_row(*svc)

    console.print(table)
    console.print(f"\n[dim]Total: {len(services_data)} services[/dim]")


@services.command()
@click.argument("name")
def describe(name: str) -> None:
    """
    Show detailed information about a service.

    \b
    Example:
      $ finops services describe trading-api
    """
    console.print(f"\n[bold blue]📊 Service: {name}[/bold blue]\n")

    # Service info table
    info_table = Table(show_header=False, box=None)
    info_table.add_column("Property", style="cyan")
    info_table.add_column("Value")

    info_table.add_row("Name", name)
    info_table.add_row("Template", "python-microservice")
    info_table.add_row("Team", "backend")
    info_table.add_row("Owner", "john.doe@example.com")
    info_table.add_row("Repository", f"https://github.com/org/{name}")
    info_table.add_row("Created", "2024-01-01")

    console.print(info_table)

    # Deployments table
    console.print("\n[bold]Deployments:[/bold]")
    deploy_table = Table()
    deploy_table.add_column("Environment")
    deploy_table.add_column("Version")
    deploy_table.add_column("Replicas")
    deploy_table.add_column("Status")
    deploy_table.add_column("URL")

    deploy_table.add_row("dev", "v1.2.3", "2/2", "✅ Healthy", f"https://{name}.dev.example.com")
    deploy_table.add_row("staging", "v1.2.3", "2/2", "✅ Healthy", f"https://{name}.staging.example.com")
    deploy_table.add_row("prod", "v1.2.2", "3/3", "✅ Healthy", f"https://{name}.example.com")

    console.print(deploy_table)

    # Dependencies
    console.print("\n[bold]Dependencies:[/bold]")
    console.print("  • PostgreSQL 15 (managed)")
    console.print("  • Redis 7 (managed)")
    console.print("  • user-service (internal)")


@services.command()
@click.argument("name")
@click.option("--force", "-f", is_flag=True, help="Force deletion")
def delete(name: str, force: bool) -> None:
    """
    Delete a service from the platform.

    \b
    Example:
      $ finops services delete old-service
      $ finops services delete old-service --force
    """
    if not force:
        if not click.confirm(f"Are you sure you want to delete '{name}'?"):
            console.print("[yellow]Deletion cancelled[/yellow]")
            return

    console.print(f"\n[bold red]🗑️ Deleting service: {name}[/bold red]\n")
    console.print("[green]✓ Service deleted successfully[/green]")


@services.command()
@click.argument("name")
@click.option("--env", "-e", default="dev", help="Environment")
@click.option("--follow", "-f", is_flag=True, help="Follow log output")
@click.option("--tail", "-n", default=100, help="Number of lines")
def logs(name: str, env: str, follow: bool, tail: int) -> None:
    """
    View service logs.

    \b
    Example:
      $ finops services logs trading-api --env dev
      $ finops services logs trading-api -e prod -f
    """
    console.print(f"\n[bold blue]📋 Logs: {name} ({env})[/bold blue]\n")

    # Sample log output
    logs_data = [
        "2024-01-15 10:30:00.123 INFO  [main] Application starting",
        "2024-01-15 10:30:00.456 INFO  [main] Connected to database",
        "2024-01-15 10:30:00.789 INFO  [main] Server listening on :8080",
        "2024-01-15 10:30:15.123 INFO  [http] GET /health 200 2ms",
        "2024-01-15 10:30:30.456 INFO  [http] POST /api/v1/trades 201 45ms",
    ]

    for log in logs_data:
        console.print(f"[dim]{log}[/dim]")
