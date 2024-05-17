# standard library
from typing import TYPE_CHECKING, cast

# pypi/conda library
from click import secho

if TYPE_CHECKING:
    # pypi/conda library
    from click import Context

    # ddpaw library
    from ddpaw.typed import MetricAPIResp, Serializable


def analyze_perf(ctx: "Context", resp: "Serializable"):
    """
    Analyze RPS, Latency or any metrics for two versions.
    Running this function required scipy
    Run `pip install --no-cache-dir "ddpaw[fast]"` or `pip install --no-cache-dir scipy==1.13`
    """
    try:
        # pypi/conda library
        import numpy as np  # noqa: F401
        from scipy import stats  # noqa: F401

        use_naive = False
    except ImportError:
        secho(
            'To perf the benchmarks faster and more robust, you can install extra some extra scientific dependencies. Please run `pip install --no-cache "ddpaw[fast]"` or `pip install --no-cache "ddpaw[all]"`. Without having the dependencies, falling back to analyze with pure python implementation.',
            fg="yellow",
            bold=True,
        )
        use_naive = True

    data = cast("MetricAPIResp", resp.to_dict())

    if (series := data.get("series", [])) and len(series) == 0:
        secho(f"no data from the query: {ctx.obj['query']}", fg="blue")
        ctx.abort()

    try:
        series_a = series[0]
        series_b = series[1]
        tag_a = next(iter(series[0].get("tag_set", [])), "version A")
        tag_b = next(iter(series[1].get("tag_set", [])), "version B")

        if tag_a == "version A" or tag_b == "version B":
            secho("warning: unable to retrieve tag_set, going to put the metric name as version X", fg="yellow")
    except KeyError:
        secho("m", fg="red", bold=True)
        ctx.abort()

    # retrieve perfs
    metrics_a = [pair[1] for pair in series_a["pointlist"]]
    metrics_b = [pair[1] for pair in series_b["pointlist"]]

    if None in metrics_a:
        secho(f"time serise of `{tag_a}` contains None value. Try to shrink the comparison window and retry", fg="red")
        ctx.abort()
    elif None in metrics_b:
        secho(f"time serise of `{tag_b}` contains None value. Try to shrink the comparison window and retry", fg="red")
        ctx.abort()

    if use_naive:
        return _analyze_perf_naive(metrics_a=metrics_a, metrics_b=metrics_b, tag_a=tag_a, tag_b=tag_b)
    return _analyze_perf_fast(metrics_a=metrics_a, metrics_b=metrics_b, tag_a=tag_a, tag_b=tag_b)


def _analyze_perf_fast(metrics_a: list[float], metrics_b: list[float], tag_a: str, tag_b: str):
    # pypi/conda library
    import numpy as np
    from scipy import stats

    # Calculate mean of metrics
    metric_a_mean = np.mean(metrics_a)
    metric_b_mean = np.mean(metrics_b)

    # Perform t-tests to compare Metrics
    metrics_ttest = stats.ttest_ind(metrics_a, metrics_b, nan_policy="raise")

    # Print comparison and statistical test results
    secho("mean of the metrics:", fg="blue", bold=True)
    secho(f"  - {tag_a}: {metric_a_mean:.2f}", fg="green", bold=True)
    secho(f"  - {tag_b}: {metric_b_mean:.2f}", fg="green", bold=True)

    secho("\n---------------------------\n")

    secho("results of the ttest:", fg="blue", bold=True)
    secho(f"  - statistic: {metrics_ttest.statistic}", fg="green", bold=True)  # type: ignore
    secho(f"  - p value: {metrics_ttest.pvalue}", fg="green", bold=True)  # type: ignore
    secho(f"  - confidence interval: {metrics_ttest.confidence_interval()}", fg="green", bold=True)  # type: ignore
    secho(f"  - df: {metrics_ttest.df}", fg="green", bold=True)  # type: ignore


def _analyze_perf_naive(metrics_a: list[float], metrics_b: list[float], tag_a: str, tag_b: str): ...
