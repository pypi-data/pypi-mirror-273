# standard library
from typing import TYPE_CHECKING, Literal

# pypi/conda library
import click
from click import secho
from datadog_api_client.v1.api.metrics_api import MetricsApi

# ddpaw library
from ddpaw.analysis import analyze_perf
from ddpaw.datastructure import Configuration
from ddpaw.typed import accept_time_format
from ddpaw.utils import plot_data, save_file

if TYPE_CHECKING:
    # standard library
    from datetime import datetime

    # pypi/conda library
    from click import Context


"""
example query:
    - sum:trace.fastapi.request.hits{env:prod,service:d2api-api} by {version}.as_rate()
    - p95:trace.fastapi.request{env:prod,service:d2api-api} by {version}

example prompt:
    - ddpaw -s 2024-04-05T12:00:00 -e 2024-04-05T17:30:00 -q "sum:trace.fastapi.request.hits{env:prod,service:d2api-api} by {version}.as_rate()"
"""


@click.group(name="ddpaw")
@click.pass_context
def cli(ctx: "Context"):
    """
    ddpaw is a command-line tool for extracting metrics from Datadog based on a query.

    It provides a set of commands to help you manage and interact with the metrics data.
    For example, you can use ddpaw to easily retrieve and analyze metrics data from Datadog.

    Usage:
        ddpaw <command> [options]

    Examples:

        ddpaw export -q "avg:system.cpu.usage{host:host0}" --format=csv --start="2022-01-01" --end="2022-01-31"

        ddpaw visualize -q "avg:system.cpu.usage{host:host0}" --start="2022-01-01" --end="2022-01-31"

        ddpaw analyze -q "avg:system.cpu.usage{host:host0}" --start="2022-01-01" --end="2022-01-31"

    Use "ddpaw <command> --help" for more information about a specific command.

    """
    ctx.ensure_object(dict)
    conf = Configuration()  # type: ignore
    ctx.obj["conf"] = conf


@cli.command(help="Export metrics data")
@click.pass_context
@click.option(
    "start_at", "-s", type=click.DateTime(accept_time_format), required=True, help="The start time of the time range."
)
@click.option(
    "end_at", "-e", type=click.DateTime(accept_time_format), required=True, help="The end time of the time range."
)
@click.option("query", "-q", type=click.STRING, required=True, help="The query to retrieve metrics data.")
@click.option(
    "format",
    "--format",
    type=click.Choice(["csv", "json"], case_sensitive=False),
    help="The format of the data.",
)
@click.option("allresp", "--all-response", is_flag=True, default=False, type=click.BOOL)
@click.option(
    "verbose",
    "-v",
    is_flag=True,
    default=False,
    type=click.BOOL,
    help="Flag indicating whether to display verbose output.",
)
def export(
    ctx: "Context",
    start_at: "datetime",
    end_at: "datetime",
    query: str,
    format: Literal["json", "csv"],
    allresp: bool,
    verbose: bool,
):
    """
    Export metrics data based on the given query and time range.

    Args:
        ctx (Context): The click context object.
        start_at (datetime): The start time of the time range.
        end_at (datetime): The end time of the time range.
        query (str): The query to retrieve metrics data.
        format(csv, json): export data and save to csv or json format, etc
        verbose (bool): Flag indicating whether to display verbose output.

    Returns:
        None

    """
    conf: Configuration = ctx.obj["conf"]
    ctx.obj["query"] = query
    ctx.obj["verbose"] = verbose

    api_client = conf.get_client()
    metrics_api = MetricsApi(api_client)
    resp = metrics_api.query_metrics(
        _from=int(start_at.timestamp()),
        to=int(end_at.timestamp()),
        query=query,
    )

    if format == "csv" and allresp:
        secho("saving all response is only avaiable for json format.", fg="yellow")
        secho("this flag will be ignored.", fg="yellow")

    if verbose:
        secho(resp)

    save_file(ctx, format=format, resp=resp, allresp=allresp)


@cli.command(help="Visualize metrics data")
@click.pass_context
@click.option(
    "start_at", "-s", type=click.DateTime(accept_time_format), required=True, help="The start time of the time range."
)
@click.option(
    "end_at", "-e", type=click.DateTime(accept_time_format), required=True, help="The end time of the time range."
)
@click.option("query", "-q", type=click.STRING, required=True, help="The query to retrieve metrics data.")
@click.option(
    "verbose",
    "-v",
    is_flag=True,
    default=False,
    type=click.BOOL,
    help="Flag indicating whether to display verbose output.",
)
def visualize(ctx: "Context", start_at: "datetime", end_at: "datetime", query: str, verbose: bool):
    conf: Configuration = ctx.obj["conf"]
    ctx.obj["query"] = query
    ctx.obj["verbose"] = verbose

    api_client = conf.get_client()
    metrics_api = MetricsApi(api_client)
    resp = metrics_api.query_metrics(
        _from=int(start_at.timestamp()),
        to=int(end_at.timestamp()),
        query=query,
    )

    plot_data(ctx=ctx, resp=resp)


@cli.command(help="Analyze metrics data")
@click.pass_context
@click.option(
    "start_at", "-s", type=click.DateTime(accept_time_format), required=True, help="The start time of the time range."
)
@click.option(
    "end_at", "-e", type=click.DateTime(accept_time_format), required=True, help="The end time of the time range."
)
@click.option("query", "-q", type=click.STRING, required=True, help="The query to retrieve metrics data.")
@click.option(
    "verbose",
    "-v",
    is_flag=True,
    default=False,
    type=click.BOOL,
    help="Flag indicating whether to display verbose output.",
)
def analyze(ctx: "Context", start_at: "datetime", end_at: "datetime", query: str, verbose: bool):
    conf: Configuration = ctx.obj["conf"]
    ctx.obj["query"] = query
    ctx.obj["verbose"] = verbose

    api_client = conf.get_client()
    metrics_api = MetricsApi(api_client)
    resp = metrics_api.query_metrics(
        _from=int(start_at.timestamp()),
        to=int(end_at.timestamp()),
        query=query,
    )

    analyze_perf(ctx=ctx, resp=resp)


@cli.command(help="Generate SHELL's completion")
@click.option(
    "verbose",
    "-v",
    is_flag=True,
    default=False,
    type=click.BOOL,
    help="Flag indicating whether to display verbose output.",
)
@click.argument("shell", type=click.STRING)
def completions(verbose: bool, shell: str):
    match shell:
        case "bash":
            secho("""
Completion for Bash

Method 1.

Add this to ~/.bashrc:

eval "$(_DDPAW_COMPLETE=bash_source ddpaw)"

------

Method 2.

Save the script somewhere.

_DDPAW_COMPLETE=bash_source ddpaw > ~/.ddpaw-complete.bash
Source the file in ~/.bashrc.

. ~/.ddpaw-complete.bash
""")
        case "zsh":
            secho("""
Completion for Zsh

Method 1.

Add this to ~/.zshrc:

eval "$(_DDPAW_COMPLETE=zsh_source ddpaw)"

---

Save the script somewhere.

_DDPAW_COMPLETE=zsh_source ddpaw > ~/.ddpaw-complete.zsh
Source the file in ~/.zshrc.

. ~/.ddpaw-complete.zsh
""")
        case "fish":
            secho("""
Completion for Fish

Add this to ~/.config/fish/completions/ddpaw.fish:

_DDPAW_COMPLETE=fish_source ddpaw | source
""")
        case _:
            secho("unable to determine the SHELL type.")


if __name__ == "__main__":
    cli()
