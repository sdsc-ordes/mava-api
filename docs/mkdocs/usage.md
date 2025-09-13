# Usage of the MAVA API

Currently only a first PoC is implemented, see [Roadmap](roadmap.md) for current status.

## Install

### Prerequisites

- Install just: https://github.com/casey/just: just is a command runner
- Install Nix: https://docs.determinate.systems/: Nix is a tool for package management that uses declarative language to provide reproducible systems
- Install Direnv: https://direnv.net/docs/installation.html: direnv is an open source environment management tool that allows setting unique environment variables per directory in your file system


### Installation

First, clone the repository to your local machine:

```sh
git clone [https://github.com/sdsc-ordes/mava-api.git](https://github.com/sdsc-ordes/mava-api.git)

All the following commands must be run from inside the project's root directory.

```sh
cd mava-api
just build
just run
```

### Serve

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

### API usage

!!! note

    For your convenience there are just command that show you how to call the api with curl. You will get the curl command that was executed printed out before the output. You can directly copy, customize and use the curl command with your own files.

### Check

Check the API status and current graph size.

```
╰─❯ just status
>> Checking API status...
curl -sS http://localhost:8000 | jq
{
  "status": "ok",
  "graph_size": 0
}
```

### Import

These imports have default files from the `examples` directory. You can also add your own custom files on the import commands as argument. Then your file will be imported instead.

**Turtle**

```
╰─❯ just import
curl -sS -X POST http://localhost:8000/graph/add -H "Content-Type: text/turtle" -d @examples/input/corpus.ttl | jq
{
  "message": "Data added successfully",
  "new_graph_size": 1
}
```

**TSV**

For TSV imports you neede to provide a json mapping so that the columns in the tsv file can be mapped to the ontology:

<details>

<summary>observations.tsv</summary>

```
start_in_seconds	start_hh:mm:ss.ms	annotations
0.0	00:00:00.0	0.11306
0.5	00:00:00.500	0.11352
1.0	00:00:01.0	0.16284
1.5	00:00:01.500	0.18034
2.0	00:00:02.0	0.18213
```

</details>

<details>

<summary>map_observations.json</summary>

```
{
  "series_description": "Cityview",
  "value_description": "probability for Cityview",
  "value_type": "numeric",
  "time_column": "start_in_seconds",
  "value_column": "annotations"
}
```
</details>

```
╰─❯ just import-observations
>> Importing tabular data from 'examples/input/observations.tsv' with mapping 'examples/input/map_observations.json'...
curl -sS -X POST "http://localhost:8000/graph/import_tsv?" -F "file=@examples/input/observations.tsv" -F "mapping_json=$(< examples/input/map_observations.json)" | jq
{
  "message": "Successfully imported data from observations.tsv",
  "new_graph_size": 24
}
```

Annotations have also columns for duration of the annotation interval:

<details>

<summary>annotations.tsv</summary>

```
start_hh:mm:ss.ms	start_in_seconds	duration_hh:mm:ss.ms	duration_in_seconds	annotations
00:00:00.0	0.0	00:00:08.0	8.0	['Transcript:: Here is the first German television with the daily news.']
00:00:15.0	15.0	00:00:03.0	3.0	['Transcript:: Today in the studio, Susanne Daubner.']
00:00:18.0	18.0	00:00:04.0	4.0	['Transcript:: Good evening ladies and gentlemen, I welcome you to the daily news.']
00:00:22.0	22.0	00:00:03.0	3.0	['Transcript:: On the sixth day of the invasion in Ukraine,']
00:00:25.0	25.0	00:00:03.0	3.0	['Transcript:: the Russian troops have strengthened their attacks']
00:00:28.0	28.0	00:00:03.0	3.0	['Transcript:: and also aimed at civilian targets.']
```

</details>

<details>

<summary>map_annotations.json</summary>

```
{
  "series_description": "Transcription",
  "value_description": "transcript",
  "value_type": "string",
  "value_prefix": "Transcript:: ",
  "time_column": "start_in_seconds",
  "value_column": "annotations",
  "duration_column": "duration_in_seconds"
}
```

</details>

```
╰─❯ just import-annotations
>> Importing tabular data from 'examples/input/annotations.tsv' with mapping 'examples/input/map_annotations.json'...
curl -sS -X POST "http://localhost:8000/graph/import_tsv?" -F "file=@examples/input/annotations.tsv" -F "mapping_json=$(< examples/input/map_annotations.json)" | jq
{
  "message": "Successfully imported data from annotations.tsv",
  "new_graph_size": 57
}
```

## View

```
╰─❯ just view
>> Viewing graph...
curl -sS http://localhost:8000/graph/export
@prefix ex: <http://example.org/data/> .
@prefix mava: <http://example.org/mava/ontology#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:5041fee4-00cb-45d0-99f8-8d89fd7ae79e_point_1 a mava:ObservationPoint ;
    mava:atTime 0.0 ;
    mava:belongsToSeries ex:5041fee4-00cb-45d0-99f8-8d89fd7ae79e ;
    mava:numericValue 0.11306 .

ex:5041fee4-00cb-45d0-99f8-8d89fd7ae79e_point_2 a mava:ObservationPoint ;
    mava:atTime 0.5 ;
    mava:belongsToSeries ex:5041fee4-00cb-45d0-99f8-8d89fd7ae79e ;
    mava:numericValue 0.11352 .

ex:5041fee4-00cb-45d0-99f8-8d89fd7ae79e_point_3 a mava:ObservationPoint ;
    mava:atTime 1.0 ;
    mava:belongsToSeries ex:5041fee4-00cb-45d0-99f8-8d89fd7ae79e ;
    mava:numericValue 0.16284 .

ex:5041fee4-00cb-45d0-99f8-8d89fd7ae79e_point_4 a mava:ObservationPoint ;
    mava:atTime 1.5 ;
    mava:belongsToSeries ex:5041fee4-00cb-45d0-99f8-8d89fd7ae79e ;
    mava:numericValue 0.18034 .

ex:5041fee4-00cb-45d0-99f8-8d89fd7ae79e_point_5 a mava:ObservationPoint ;
    mava:atTime 2.0 ;
    mava:belongsToSeries ex:5041fee4-00cb-45d0-99f8-8d89fd7ae79e ;
    mava:numericValue 0.18213 .

ex:af2bf119-4c06-4bab-ab27-4b99f0aacfe8_point_1 a mava:AnnotationSegment ;
    mava:belongsToSeries ex:af2bf119-4c06-4bab-ab27-4b99f0aacfe8 ;
    mava:endTime 8.0 ;
    mava:startTime 0.0 ;
    mava:stringValue "['Transcript:: Here is the first German television with the daily news.']"^^xsd:string .

ex:af2bf119-4c06-4bab-ab27-4b99f0aacfe8_point_2 a mava:AnnotationSegment ;
    mava:belongsToSeries ex:af2bf119-4c06-4bab-ab27-4b99f0aacfe8 ;
    mava:endTime 18.0 ;
    mava:startTime 15.0 ;
    mava:stringValue "['Transcript:: Today in the studio, Susanne Daubner.']"^^xsd:string .

ex:af2bf119-4c06-4bab-ab27-4b99f0aacfe8_point_3 a mava:AnnotationSegment ;
    mava:belongsToSeries ex:af2bf119-4c06-4bab-ab27-4b99f0aacfe8 ;
    mava:endTime 22.0 ;
    mava:startTime 18.0 ;
    mava:stringValue "['Transcript:: Good evening ladies and gentlemen, I welcome you to the daily news.']"^^xsd:string .

ex:af2bf119-4c06-4bab-ab27-4b99f0aacfe8_point_4 a mava:AnnotationSegment ;
    mava:belongsToSeries ex:af2bf119-4c06-4bab-ab27-4b99f0aacfe8 ;
    mava:endTime 25.0 ;
    mava:startTime 22.0 ;
    mava:stringValue "['Transcript:: On the sixth day of the invasion in Ukraine,']"^^xsd:string .

ex:af2bf119-4c06-4bab-ab27-4b99f0aacfe8_point_5 a mava:AnnotationSegment ;
    mava:belongsToSeries ex:af2bf119-4c06-4bab-ab27-4b99f0aacfe8 ;
    mava:endTime 28.0 ;
    mava:startTime 25.0 ;
    mava:stringValue "['Transcript:: the Russian troops have strengthened their attacks']"^^xsd:string .

ex:af2bf119-4c06-4bab-ab27-4b99f0aacfe8_point_6 a mava:AnnotationSegment ;
    mava:belongsToSeries ex:af2bf119-4c06-4bab-ab27-4b99f0aacfe8 ;
    mava:endTime 31.0 ;
    mava:startTime 28.0 ;
    mava:stringValue "['Transcript:: and also aimed at civilian targets.']"^^xsd:string .

mava:Corpus1 a mava:Corpus .

ex:5041fee4-00cb-45d0-99f8-8d89fd7ae79e a mava:ObservationSeries ;
    mava:seriesDescription "Cityview" ;
    mava:valueDescription "probability for Cityview" .

ex:af2bf119-4c06-4bab-ab27-4b99f0aacfe8 a mava:AnnotationSeries ;
    mava:seriesDescription "Transcription" ;
    mava:valueDescription "transcript" .
```
## Export

Export the current graph to a Turtle file.

```
╰─❯ just export
>> Exporting graph to 'examples/output/export.ttl'...
curl -sS -o examples/output/export.ttl http://localhost:8000/graph/export
Done.
```

## Clear

Clear the current graph to start from scratch.

```
╰─❯ just clear
>> Clearing graph...
curl -sS -X DELETE http://localhost:8000/graph/clear | jq
{
  "message": "Graph cleared successfully"
}
```
<script src="https://hypothes.is/embed.js" async></script>
