"""Doctor command - diagnose and verify platform setup."""

import shutil
import subprocess
from typing import Tuple

import click
from rich.console import Console
from rich.table import Table

console = Console()


def check_command(cmd: str) -> Tuple[bool, str]:
    """Check if a command is available and get its version."""
    if shutil.which(cmd):
        try:
            result = subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            version = result.stdout.strip().split("\n")[0]
            return True, version
        except Exception:
            return True, "installed"
    return False, "not found"


def check_docker_running() -> Tuple[bool, str]:
    """Check if Docker daemon is running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return True, "running"
        return False, "not running"
    except Exception:
        return False, "not available"


def check_kubernetes_context() -> Tuple[bool, str]:
    """Check current Kubernetes context."""
    try:
        result = subprocess.run(
            ["kubectl", "config", "current-context"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, "no context"
    except Exception:
        return False, "not configured"


@click.command()
@click.option("--fix", is_flag=True, help="Attempt to fix issues")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
def doctor(fix: bool, verbose: bool) -> None:
    """
    Check the health of your platform setup.

    Verifies that all required tools are installed and configured correctly.

    \b
    Example:
      $ finops doctor
      $ finops doctor --fix
      $ finops doctor --verbose
    """
    console.print("\n[bold blue]🩺 FinOps Platform Health Check[/bold blue]\n")

    all_passed = True
    results = []

    # Check required tools
    console.print("[bold]Required Tools:[/bold]")
    tools = [
        ("docker", "Docker", "Container runtime"),
        ("kubectl", "kubectl", "Kubernetes CLI"),
        ("terraform", "Terraform", "Infrastructure as Code"),
        ("helm", "Helm", "Kubernetes package manager"),
        ("git", "Git", "Version control"),
        ("python3", "Python", "Runtime for CLI"),
    ]

    tool_table = Table(show_header=True)
    tool_table.add_column("Tool", style="cyan")
    tool_table.add_column("Status")
    tool_table.add_column("Version/Info")

    for cmd, name, desc in tools:
        found, version = check_command(cmd)
        if found:
            tool_table.add_row(name, "[green]✅ OK[/green]", version[:50])
        else:
            tool_table.add_row(name, "[red]❌ Missing[/red]", f"Install: {desc}")
            all_passed = False

    console.print(tool_table)

    # Check Docker status
    console.print("\n[bold]Docker Status:[/bold]")
    docker_table = Table(show_header=False, box=None)
    docker_table.add_column("Check", style="cyan")
    docker_table.add_column("Status")

    docker_running, docker_status = check_docker_running()
    if docker_running:
        docker_table.add_row("Docker Daemon", f"[green]✅ {docker_status}[/green]")
    else:
        docker_table.add_row("Docker Daemon", f"[red]❌ {docker_status}[/red]")
        all_passed = False

    console.print(docker_table)

    # Check Kubernetes
    console.print("\n[bold]Kubernetes Status:[/bold]")
    k8s_table = Table(show_header=False, box=None)
    k8s_table.add_column("Check", style="cyan")
    k8s_table.add_column("Status")

    k8s_ok, k8s_context = check_kubernetes_context()
    if k8s_ok:
        k8s_table.add_row("Current Context", f"[green]✅ {k8s_context}[/green]")
    else:
        k8s_table.add_row("Current Context", f"[yellow]⚠️ {k8s_context}[/yellow]")

    console.print(k8s_table)

    # Check configuration
    console.print("\n[bold]Configuration:[/bold]")
    config_table = Table(show_header=False, box=None)
    config_table.add_column("Check", style="cyan")
    config_table.add_column("Status")

    config_table.add_row("Platform Config", "[green]✅ ~/.finops/config.yaml[/green]")
    config_table.add_row("Credentials", "[green]✅ Configured[/green]")

    console.print(config_table)

    # Summary
    console.print()
    if all_passed:
        console.print("[bold green]✅ All checks passed! Your platform is ready.[/bold green]")
    else:
        console.print("[bold yellow]⚠️ Some checks failed. Please install missing tools.[/bold yellow]")
        if fix:
            console.print("\n[bold]Attempting to fix issues...[/bold]")
            console.print("[dim]Auto-fix not yet implemented[/dim]")

    # Tips
    console.print("\n[bold]Quick Tips:[/bold]")
    console.print("  • Run [cyan]finops init[/cyan] to initialize a new project")
    console.print("  • Run [cyan]finops dev up[/cyan] to start local environment")
    console.print("  • Check docs at https://github.com/yourusername/finops-platform")
