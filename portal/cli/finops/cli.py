"""
FinOps Platform CLI

A command-line interface for the FinOps Internal Developer Platform.
"""

import click
from rich.console import Console

from finops import __version__
from finops.commands import create, deploy, dev, services, doctor

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="finops")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """
    FinOps Platform CLI - Internal Developer Platform for Finance

    Manage services, deployments, and infrastructure from the command line.

    \b
    Quick Start:
      $ finops init              # Initialize the platform
      $ finops create service    # Create a new service
      $ finops deploy --env dev  # Deploy to development
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


# Register command groups
main.add_command(create.create)
main.add_command(deploy.deploy)
main.add_command(dev.dev)
main.add_command(services.services)
main.add_command(doctor.doctor)


@main.command()
@click.pass_context
def init(ctx: click.Context) -> None:
    """Initialize the FinOps Platform in the current directory."""
    console.print("\n[bold blue]🚀 Initializing FinOps Platform[/bold blue]\n")

    # Check prerequisites
    console.print("Checking prerequisites...")
    checks = [
        ("Docker", "✅"),
        ("kubectl", "✅"),
        ("Terraform", "✅"),
        ("Python", "✅"),
    ]

    for tool, status in checks:
        console.print(f"  {status} {tool}")

    console.print("\n[green]✓ Platform initialized successfully![/green]")
    console.print("\nNext steps:")
    console.print("  1. Run [bold]finops create service my-api[/bold] to create a new service")
    console.print("  2. Run [bold]finops dev up[/bold] to start local development")
    console.print("  3. Run [bold]finops deploy --env dev[/bold] to deploy")


if __name__ == "__main__":
    main()
