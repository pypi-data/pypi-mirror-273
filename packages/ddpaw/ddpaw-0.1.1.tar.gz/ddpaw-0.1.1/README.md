# DDPaw CLI Tool

## Description

`ddpaw` is a command-line tool for extracting, visualizing, and analyzing metrics from Datadog's Application Performance Monitoring (APM) service based on a query. It provides a set of commands to help you manage and interact with metrics data.



## Table of Contents

[TOC]

## Installation

```bash
pip install --no-cache-dir ddpaw
```



## Usage

`ddpaw` provides several commands to interact with Datadog metrics

```bash
ddpaw <command> [options]
```

Set up your DataDog API credentials by creating a `.env` file in the project root directory:

```bash
API_KEY=your-api-key
APP_KEY=your-app-key
```



### Commands

#### export

> Export metrics data based on the given query and time range.

##### Options

- `-s`, `--start_at`: The start time of the time range (required).
- `-e`, `--end_at`: The end time of the time range (required).
- `-q`, `--query`: The query to retrieve metrics data (required).
- `--format`: The format of the data (choices: `csv`, `json`).
- `--all-response`: Flag indicating whether to include all response data.
- `-v`, `--verbose`: Flag indicating whether to display verbose output.

##### Example

```bash
ddpaw export -s 2024-04-05T12:00:00 -e 2024-04-05T17:30:00 \
						 -q "sum:trace.fastapi.request.hits{env:prod,service:d2api-api} by {version}.as_rate()" \
						 --format=csv
```



#### visualize

Visualize metrics data based on the given query and time range.

##### Options

- `-s`, `--start_at`: The start time of the time range (required).
- `-e`, `--end_at`: The end time of the time range (required).
- `-q`, `--query`: The query to retrieve metrics data (required).
- `-v`, `--verbose`: Flag indicating whether to display verbose output.

##### Example

```bash
ddpaw visualize -s 2024-04-05T12:00:00 -e 2024-04-05T17:30:00 \
							  -q "sum:trace.fastapi.request.hits{env:prod,service:d2api-api} by {version}.as_rate()"
```



### analyze

Analyze metrics data based on the given query and time range.

##### Options

- `-s`, `--start_at`: The start time of the time range (required).
- `-e`, `--end_at`: The end time of the time range (required).
- `-q`, `--query`: The query to retrieve metrics data (required).
- `-v`, `--verbose`: Flag indicating whether to display verbose output.

##### Example

```bash
ddpaw analyze -s 2024-04-05T12:00:00 -e 2024-04-05T17:30:00 \
							-q "sum:trace.fastapi.request.hits{env:prod,service:d2api-api} by {version}.as_rate()"
```



### Completions

Generate shell completions for `ddpaw`.

#### Arguments

- `shell`: The shell type (choices: `bash`, `zsh`, `fish`).

For example:

```bash
ddpaw completions bash
```



## Contributing

Contributions are welcome! Please follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).



## License

This project is licensed under the [MIT License](LICENSE).
