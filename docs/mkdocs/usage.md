# Usage of the MAVA API

Currently only a first PoC is implemented, see [Roadmap](roadmap.md) for current status

## Step 1: Install

### Prerequisites
This repository relies on `nix` and `direnv`.

### Install

First, clone the repository to your local machine:

```sh
git clone [https://github.com/sdsc-ordes/mava-api.git](https://github.com/sdsc-ordes/mava-api.git)

All the following commands must be run from inside the project's root directory.

```sh
cd mava-api
just build
just run
```

## Step 2: Start the API

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

!!! note

    All graph building steps can be repeated as often as you want. THe graph will not get confused and will only add new metadata.

## Step 3: check the current status

```
╰─❯ just status
>> Checking API status...
{
  "status": "ok",
  "graph_size": 0
}
```

## Step 4: Import Turtle or CSV files

These imports default files from the `examples` directory. You can also add your own custom files on the import commands as argument. Then your file will be imported instead.

```
╰─❯ just import
>> Importing data from 'examples/input/input.ttl'...
{
  "message": "Data added successfully",
  "new_graph_size": 1
}
```

```
╰─❯ just import-csv
>> Importing data from CSV file 'examples/input/input.csv'...
{
  "message": "Successfully imported data from input.csv",
  "new_graph_size": 11
}
```
## Step 5: Inspect the graph

```
╰─❯ just view
>> Viewing graph...
@prefix ex: <http://example.org/data/> .
@prefix mava: <http://example.org/mava/ontology#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:input_point_1 a mava:DataPoint ;
    mava:atTime 1.75 ;
    mava:belongsToSeries ex:input ;
    mava:numericValue 0.88385 .

ex:input_point_2 a mava:DataPoint ;
    mava:atTime 5.75 ;
    mava:belongsToSeries ex:input ;
    mava:numericValue 0.65886 .

mava:Corpus1 a mava:Corpus .

ex:input a mava:DataSeries ;
    mava:seriesType "Voice Activity Score" .
```
## Step 6: Export the graph

```
╰─❯ just export
>> Exporting graph to 'examples/output/export.ttl'...
Done.
```

## Step 7:  Clear the graph

```
╰─❯ just clear
>> Clearing graph...
{
  "message": "Graph cleared successfully"
}
```
!!! warning

    The csv import is not very flexible yet. Mapping csv field will come in the next milestone, see [roadmap](roadmap.md)
