# Install

## Prerequisites

- [Install just](https://github.com/casey/just): just is a command runner
- [Install Nix](https://docs.determinate.systems/): Nix is a tool for package management that uses declarative language to provide reproducible systems
- [Install Direnv](https://direnv.net/docs/installation.html): direnv is an open source environment management tool that allows setting unique environment variables per directory in your file system


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

Set up docs locally you have two steps:

- build all docs with `just docs build`
- serve mkdocs with `just docs serve`
- then the documentation will be available at `http://127.0.0.1:8001/mava-api/docs/` or open `site/docs/index.html` with a browser of your choice


```hl_lines="1 7 9" title="Build all docs"
╰─❯ just docs build
>> Cleaning old site directory...site
>> Building ontology documentation...
>> Ontology documentation available at site/ontology/index.html
>> Generating OpenAPI specification...
>> Building MkDocs site...
>> Documentation site successfully built in 'site' directory.
```

```hl_lines="1 7" title="Serve mkdocs"
╰─❯ just docs serve
>> Serving documentation...
uv run mkdocs serve -f docs/mkdocs.yml -a 127.0.0.1:8001
INFO    -  Building documentation...
INFO    -  Cleaning site directory
INFO    -  [11:54:50] Watching paths for changes: 'docs/mkdocs', 'docs/mkdocs.yml'
INFO    -  [11:54:50] Serving on http://127.0.0.1:8001/mava-api/docs/
```
