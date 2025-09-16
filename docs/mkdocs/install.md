# Install

## Prerequisites

- Install just: https://github.com/casey/just: just is a command runner
- Install Nix: https://docs.determinate.systems/: Nix is a tool for package management that uses declarative language to provide reproducible systems
- Install Direnv: https://direnv.net/docs/installation.html: direnv is an open source environment management tool that allows setting unique environment variables per directory in your file system


## Installation

First, clone the repository to your local machine:

```sh
git clone [https://github.com/sdsc-ordes/mava-api.git](https://github.com/sdsc-ordes/mava-api.git)

All the following commands must be run from inside the project's root directory.

```sh
cd mava-api
just build
just run
```

## Serve

- `just run`

```
╰─❯ just run
uv run uvicorn src.mava.main:app --reload "$@"
INFO:     Will watch for changes in these directories: ['/Users/smaennel/WORK/MAVA/mava-api']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [50168] using WatchFiles
INFO:     Started server process [50170]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

The server should now be running at `http://127.0.0.1:8000`.

## Docs

