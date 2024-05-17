# standard library
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Literal, cast

# pypi/conda library
from click import secho

if TYPE_CHECKING:
    # pypi/conda library
    from click import Context

    # ddpaw library
    from ddpaw.typed import MetricAPIResp, Serializable


def save_file(ctx: "Context", filename: str, format: Literal["json", "csv"], resp: "Serializable", allresp: bool):
    output = Path().cwd() / f"{filename}.{format}"
    output.parent.mkdir(parents=True, exist_ok=True)
    data = cast("MetricAPIResp", resp.to_dict())

    match format:
        case "json":
            if allresp:
                output.write_text(json.dumps(data, indent=2))
            else:
                series = data.get("series", [])
                pointlists = [serie["pointlist"] for serie in series if "pointlist" in serie]
                output.write_text(json.dumps(pointlists, indent=2))

        case "csv":
            columns = ["timestamp", "value"]

            if (series := data.get("series", [])) and len(series) == 0:
                secho(f"no data from the query: {ctx.obj['query']}", fg="blue")
                ctx.abort()

            with output.open(mode="w") as file:
                writer = csv.writer(file)
                writer.writerow(columns)

                for serie in series:
                    pointlist: list[tuple[float, float]] = serie.get("pointlist", [])
                    if len(pointlist) == 0:
                        continue
                    [writer.writerow(row) for row in pointlist]

        case _:
            raise NotImplementedError

    secho(f"done! file is saved at {output}")


def plot_data(ctx: "Context", resp: "Serializable"):
    try:
        # pypi/conda library
        import matplotlib.dates as mdates  # pyright: ignore
        import matplotlib.pyplot as plt  # pyright: ignore
        import seaborn as sns  # pyright: ignore
    except ImportError:
        secho(
            'To plot the metrics, you will need to install extra some extra dependencies. Please run `pip install --no-cache "ddpaw[plot]"` or `pip install --no-cache "ddpaw[all]"`.',
            fg="yellow",
            bold=True,
        )
        ctx.abort()

    data = cast("MetricAPIResp", resp.to_dict())

    if (series := data.get("series", [])) and len(series) == 0:
        secho(f"no data from the query: {ctx.obj['query']}", fg="blue")
        ctx.abort()

    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(10, 6))

    for serie in series:
        # expr = serie.get("expression", "")
        # metric = serie.get("metric", "")
        pointlist: list[tuple[float, float]] = serie.get("pointlist", [])

        if len(pointlist) == 0:
            continue

        x_labels = [datetime.fromtimestamp(pair[0] / 1000) for pair in (pointlist)]
        y_values = [pair[1] for pair in pointlist]

        sns.lineplot(x=x_labels, y=y_values)

        # Formatting the date axis
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.gca().xaxis.set_major_formatter(mdates.ConciseDateFormatter(mdates.AutoDateLocator()))
        plt.gcf().autofmt_xdate()  # Rotate date labels to prevent overlap

        # Filling the area under the curve
        plt.fill_between(x_labels, y_values, alpha=0.4)

        plt.xlabel("Time")
        plt.ylabel("Metric")
        plt.title("Application Metric Over Time")
        plt.tight_layout()

    plt.show()
