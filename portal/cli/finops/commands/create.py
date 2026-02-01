"""Create command - scaffold new services and resources."""

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

TEMPLATES = {
    "python-microservice": {
        "description": "FastAPI microservice with PostgreSQL",
        "stack": ["Python 3.11", "FastAPI", "PostgreSQL", "Redis"],
    },
    "node-microservice": {
        "description": "Express.js service with MongoDB",
        "stack": ["Node.js 20", "Express", "MongoDB", "Redis"],
    },
    "event-processor": {
        "description": "Kafka event processor",
        "stack": ["Python 3.11", "Kafka", "Redis"],
    },
    "batch-job": {
        "description": "Scheduled batch processing job",
        "stack": ["Python 3.11", "Airflow", "PostgreSQL"],
    },
}


@click.group()
def create() -> None:
    """Create new services, resources, and configurations."""
    pass


@create.command()
@click.argument("name")
@click.option(
    "--template",
    "-t",
    type=click.Choice(list(TEMPLATES.keys())),
    default="python-microservice",
    help="Service template to use",
)
@click.option("--description", "-d", default="", help="Service description")
@click.option("--team", default="platform", help="Team ownership")
@click.option("--output", "-o", default=".", help="Output directory")
def service(name: str, template: str, description: str, team: str, output: str) -> None:
    """
    Create a new service from a template.

    \b
    Example:
      $ finops create service my-trading-api --template python-microservice
      $ finops create service payment-processor -t event-processor
    """
    template_info = TEMPLATES[template]

    console.print(f"\n[bold blue]🔨 Creating service: {name}[/bold blue]\n")
    console.print(Panel(f"""
[bold]Template:[/bold] {template}
[bold]Description:[/bold] {template_info['description']}
[bold]Stack:[/bold] {', '.join(template_info['stack'])}
[bold]Team:[/bold] {team}
    """, title="Service Configuration"))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Creating service structure...", total=5)

        # Simulate creation steps
        import time

        steps = [
            "Creating directory structure",
            "Generating source files",
            "Setting up CI/CD pipelines",
            "Configuring Kubernetes manifests",
            "Initializing Git repository",
        ]

        for step in steps:
            progress.update(task, description=step)
            time.sleep(0.3)
            progress.advance(task)

    console.print(f"\n[green]✓ Service '{name}' created successfully![/green]\n")
    console.print("Next steps:")
    console.print(f"  1. cd {name}")
    console.print("  2. finops dev up")
    console.print("  3. Open http://localhost:8000/docs")


@create.command()
@click.argument("name")
@click.option("--type", "resource_type", type=click.Choice(["database", "cache", "queue", "storage"]))
def resource(name: str, resource_type: str) -> None:
    """Create a new infrastructure resource."""
    console.print(f"\n[bold blue]🔧 Creating {resource_type}: {name}[/bold blue]\n")
    console.print(f"[green]✓ Resource '{name}' configuration created![/green]")
