# standard library
from datetime import datetime
from typing import Any, Protocol, TypedDict

datelike = str | int | datetime

accept_time_format = [
    "%Y-%m-%d",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d-%H:%M:%S",
    "%Y-%m-%d_%H:%M:%S",
]


class Serie(TypedDict):
    attributes: dict[Any, Any]
    aggr: str
    display_name: str
    start: int
    end: int
    expression: str
    interval: int
    lengh: int
    metric: str
    pointlist: list[tuple[float, float]]
    scope: str
    tag_set: list[str]


class MetricAPIResp(TypedDict):
    resp_version: int
    values: list[int]
    times: list[int]
    from_date: int
    group_by: list[str]
    message: str
    query: str
    res_type: str
    series: list[Serie]
    status: str
    to_date: str


class Serializable(Protocol):
    def to_dict(self) -> dict[Any, Any]: ...
