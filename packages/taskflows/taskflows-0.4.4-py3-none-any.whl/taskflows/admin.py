import re
import subprocess
from functools import lru_cache
from itertools import cycle
from pprint import pformat, pprint
from typing import Optional, Tuple
from collections import defaultdict

import click
import sqlalchemy as sa
from click.core import Group
from dynamic_imports import import_module
from rich import box
from rich.console import Console
from rich.table import Table

from .db import task_flows_db
from .service import (
    systemd_dir,
    Service,
    disable_service,
    enable_service,
    get_service_files,
    get_timer_files,
    remove_service,
    restart_service,
    service_cmd,
    service_runs,
    start_service,
    stop_service,
)
from .utils import _SYSTEMD_FILE_PREFIX

cli = Group("taskflows", chain=True)


@cli.command()
@click.option(
    "-l",
    "--limit",
    type=int,
    default=3,
    help="Number of most recent task runs to show.",
)
@click.option(
    "-m", "--match", help="Only show history for this task name or task name pattern."
)
def history(limit: int, match: str = None):
    """Print task run history to console display."""
    # https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors
    db = task_flows_db()
    table = db.task_runs_table
    console = Console()
    column_color = table_column_colors()
    task_names_query = sa.select(table.c.task_name).distinct()
    if match:
        task_names_query = task_names_query.where(table.c.task_name.like(f"%{match}%"))
    query = (
        sa.select(table)
        .where(table.c.task_name.in_(task_names_query))
        .order_by(table.c.started.desc(), table.c.task_name)
    )
    if limit:
        query = query.limit(limit)
    columns = [c.name.replace("_", " ").title() for c in table.columns]
    with task_flows_db().engine.begin() as conn:
        rows = [dict(zip(columns, row)) for row in conn.execute(query).fetchall()]
    table = Table(title="Task History", box=box.SIMPLE)
    if all(row["Retries"] == 0 for row in rows):
        columns.remove("Retries")
    for c in columns:
        table.add_column(c, style=column_color(c), justify="center")
    for row in rows:
        table.add_row(*[str(row[c]) for c in columns])
    console.print(table, justify="center")


@cli.command
@click.argument("service_name")
def status(service_name: str):
    """Get status of service."""
    proc = service_cmd(service_name=service_name, command="status")
    pprint(proc.stderr.decode().split("\n"))
    pprint(proc.stdout.decode().split("\n"))
    # manager.GetUnitFileState(service)


@cli.command(name="list")
def list_services():
    """List services."""
    services = [f.stem.replace(_SYSTEMD_FILE_PREFIX,"") for f in get_service_files()]
    if services:
        click.echo(pformat(services))
    else:
        click.echo(click.style("No services found.", fg="yellow"))


@cli.command()
@click.option(
    "-m", "--match", help="Only show for this service name or service name pattern."
)
def schedule(match: str = None):
    """List service schedules."""
    table = _service_schedules_table(running_only=False, match=match)
    if table is not None:
        Console().print(table, justify="center")
    else:
        click.echo(click.style("No services found.", fg="yellow"))


@cli.command()
def running():
    """List running services."""
    table = _service_schedules_table(running_only=True)
    if table is not None:
        Console().print(table, justify="center")
    else:
        click.echo(click.style("No services running.", fg="yellow"))


@cli.command()
@click.argument("service_name")
def logs(service_name: str):
    """Show logs for a service."""
    click.echo(
        click.style(
            f"Run `journalctl --user -r -u {_SYSTEMD_FILE_PREFIX}{service_name}` for more.",
            fg="yellow",
        )
    )
    subprocess.run(
        f"journalctl --user -f -u {_SYSTEMD_FILE_PREFIX}{service_name}".split()
    )


@cli.command()
@click.argument("service_file", default="deployments.py")
@click.option(
    "-i",
    "--include",
    multiple=True,
    help="Name(s) of service(s)/service list(s) that should be created.",
)
@click.option(
    "-im",
    "--include-matching",
    multiple=True,
    help="Substring(s) of service(s)/service list(s) names that should be created.",
)
@click.option(
    "-e",
    "--exclude",
    multiple=True,
    help="Name(s) of service(s)/service list(s) that should not be created.",
)
@click.option(
    "-em",
    "--exclude-matching",
    multiple=True,
    help="Substring(s) of service(s)/service list(s) names that should not be created.",
)
def create(
    service_file: str,
    include: Optional[Tuple[str]] = None,
    include_matching: Optional[Tuple[str]] = None,
    exclude: Optional[Tuple[str]] = None,
    exclude_matching: Optional[Tuple[str]] = None,
):
    """Create services from a Python file containing services/service lists or dict with services or service lists as values."""
    services = {}
    for member in import_module(service_file).__dict__.values():
        if isinstance(member, Service):
            services[member.name] = member
        elif isinstance(member, (list, tuple)):
            services.update({m.name: m for m in member if isinstance(m, Service)})
        elif isinstance(member, dict):
            for k, v in member.items():
                if isinstance(v, Service):
                    services[v.name] = v
                    services[k] = v
                elif isinstance(v, (list, tuple)) and (
                    v := {m.name: m for m in v if isinstance(m, Service)}
                ):
                    services.update(v)
                    services[k] = v
    if include:
        services = {
            k: v for k, v in services.items() if any(name == k for name in include)
        }
    if include_matching:
        services = {
            k: v
            for k, v in services.items()
            if any(name in k for name in include_matching)
        }
    if exclude:
        services = {
            k: v for k, v in services.items() if not any(name == k for name in exclude)
        }
    if exclude_matching:
        services = {
            k: v
            for k, v in services.items()
            if not any(name in k for name in exclude_matching)
        }
    click.echo(
        click.style(
            f"Creating {len(services)} service(s) from {service_file}.", fg="cyan"
        )
    )
    for srv in services.values():
        srv.create()
    click.echo(click.style("Done!", fg="green"))


@cli.command()
@click.argument("service")
def start(service: str):
    """Start service(s).

    Args:
        service (str): Name or name pattern of service(s) to start.
    """
    start_service(service)
    click.echo(click.style("Done!", fg="green"))


@cli.command()
@click.argument("service")
def stop(service: str):
    """Stop running service(s).

    Args:
        service (str): Name or name pattern of service(s) to stop.
    """
    stop_service(service)
    click.echo(click.style("Done!", fg="green"))


@cli.command()
@click.argument("service")
def restart(service: str):
    """Restart running service(s).

    Args:
        service (str): Name or name pattern of service(s) to restart.
    """
    restart_service(service)
    click.echo(click.style("Done!", fg="green"))


@cli.command()
@click.argument("service")
def enable(service: str):
    """Enable currently disabled service(s).

    Args:
        service (str): Name or name pattern of service(s) to restart.
    """
    enable_service(service)
    click.echo(click.style("Done!", fg="green"))


@cli.command()
@click.argument("service")
def disable(service: str):
    """Disable service(s).

    Args:
        service (str): Name or name pattern of service(s) to disable.
    """
    disable_service(service)
    click.echo(click.style("Done!", fg="green"))


@cli.command()
@click.argument("service")
def remove(service: str):
    """Remove service(s).

    Args:
        service (str): Name or name pattern of service(s) to remove.
    """
    remove_service(service)
    click.echo(click.style("Done!", fg="green"))


@cli.command
@click.argument("service", required=False)
def show(service: str):
    files = defaultdict(list)
    for f in systemd_dir.glob(f"{_SYSTEMD_FILE_PREFIX}*.service"):
        files[f.stem].append(f)
    for f in systemd_dir.glob(f"{_SYSTEMD_FILE_PREFIX}*.timer"):
        files[f.stem].append(f)
    if service:
        files = {k: v for k, v in files.items() if service in k}
    services = []
    for srvs in files.values():
        services.append('\n'.join([s.read_text() for s in srvs]))
    services = "\n\n".join(services)
    click.echo(click.style(services, fg="cyan"))


def table_column_colors():
    colors_gen = cycle(["orange3", "green", "cyan", "magenta", "dodger_blue1", "red"])

    @lru_cache
    def column_color(col_name: str) -> str:
        return next(colors_gen)

    return column_color


def _service_schedules_table(running_only: bool, match: str = None) -> Table:
    timer_files = get_timer_files(match)
    srv_schedules = {
        re.search(r"^taskflow_([\w-]+)", f.stem)
        .group(1): re.search(r"\[Timer\]((.|\n)+)\[", f.read_text(), re.MULTILINE)
        .group(1)
        .replace("Persistent=true", "")
        .strip()
        for f in timer_files
    }
    srv_runs = service_runs(match)
    if running_only:
        srv_runs = {
            srv_name: runs
            for srv_name, runs in srv_runs.items()
            if runs.get("Last Run", "").endswith("(running)")
        }
        srv_schedules = {
            srv_name: sched
            for srv_name, sched in srv_schedules.items()
            if srv_name in srv_runs
        }
    srv_schedules = {k: v for k, v in srv_schedules.items() if v}
    if not srv_schedules:
        return
    table = Table(box=box.SIMPLE)
    column_color = table_column_colors()
    for col in ("Service", "Schedule", "Next Run", "Last Run"):
        table.add_column(col, style=column_color(col), justify="center")
    for srv_name, sched in srv_schedules.items():
        runs = srv_runs.get(srv_name, {})
        table.add_row(
            srv_name, sched, runs.get("Next Run", ""), runs.get("Last Run", "")
        )
    return table
