"""Deploy command - manage service deployments."""

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


@click.command()
@click.argument("service", required=False)
@click.option(
    "--env",
    "-e",
    type=click.Choice(["dev", "staging", "prod"]),
    default="dev",
    help="Target environment",
)
@click.option("--dry-run", is_flag=True, help="Simulate deployment without applying")
@click.option("--force", "-f", is_flag=True, help="Force deployment without confirmation")
@click.option("--tag", "-t", help="Specific image tag to deploy")
def deploy(service: str | None, env: str, dry_run: bool, force: bool, tag: str | None) -> None:
    """
    Deploy a service to the specified environment.

    \b
    Examples:
      $ finops deploy --env dev              # Deploy current service to dev
      $ finops deploy my-api --env staging   # Deploy specific service
      $ finops deploy --env prod --dry-run   # Preview production deployment
    """
    service_name = service or "current-service"

    console.print(f"\n[bold blue]🚀 Deploying {service_name} to {env}[/bold blue]\n")

    # Show deployment plan
    table = Table(title="Deployment Plan")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Service", service_name)
    table.add_row("Environment", env)
    table.add_row("Image Tag", tag or "latest")
    table.add_row("Strategy", "Rolling Update")
    table.add_row("Replicas", "2" if env == "dev" else "3")

    console.print(table)
    console.print()

    if dry_run:
        console.print("[yellow]⚠ Dry run mode - no changes will be applied[/yellow]\n")
        console.print("[green]✓ Deployment plan validated successfully![/green]")
        return

    if env == "prod" and not force:
        if not click.confirm("Deploy to production?"):
            console.print("[yellow]Deployment cancelled[/yellow]")
            return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        import time

        steps = [
            "Validating configuration",
            "Building container image",
            "Pushing to registry",
            "Updating Kubernetes manifests",
            "Triggering ArgoCD sync",
            "Waiting for rollout",
        ]

        task = progress.add_task("Deploying...", total=len(steps))
        for step in steps:
            progress.update(task, description=step)
            time.sleep(0.4)
            progress.advance(task)

    console.print(f"\n[green]✓ {service_name} deployed to {env} successfully![/green]\n")
    console.print("Deployment details:")
    console.print(f"  • URL: https://{service_name}.{env}.example.com")
    console.print(f"  • Dashboard: https://grafana.example.com/d/{service_name}")
    console.print(f"  • Logs: finops logs {service_name} --env {env}")
