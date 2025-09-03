# Use the API

api_base_url := "http://localhost:8000"
default_import_file := "examples/input/corpus.ttl"
default_export_file := "examples/output/export.ttl"
default_timeline_tsv_file := "examples/input/timeline.tsv"
default_series_tsv_file := "examples/input/series.tsv"
default_map_timeline := "examples/input/map_timeline.json"
default_map_series := "examples/input/map_series.json"

# Checks the status of the API and the current graph size
status:
    @echo ">> Checking API status..."
    @curl -sS {{api_base_url}} | jq

# Imports data from a specified Turtle file (defaults to data.ttl)
import filename=default_import_file:
    @echo ">> Importing data from '{{filename}}'..."
    @curl -sS -X POST {{api_base_url}}/graph/add \
        -H "Content-Type: text/turtle" \
        -d @{{filename}} | jq

# Imports tabular data (CSV/TSV) using a specified mapping
import-tsv file=default_series_tsv_file mapping=default_map_series:
    @echo ">> Importing tabular data from '{{file}}' with mapping '{{mapping}}'..."
    @curl -sS -X POST "{{api_base_url}}/graph/import_tsv?" \
        -F "file=@{{file}}" \
        -F "mapping_json=$(< {{mapping}})" | jq

# Exports the entire graph to a file (defaults to export.ttl)
export filename=default_export_file:
    @echo ">> Exporting graph to '{{filename}}'..."
    @curl -sS -o {{filename}} {{api_base_url}}/graph/export
    @echo "Done."

# Views graph directly in the terminal
view:
    @echo ">> Viewing graph..."
    @curl -sS {{api_base_url}}/graph/export

# Delete Graph
# Clears the entire graph on the server
clear:
    @echo ">> Clearing graph..."
    @curl -sS -X DELETE {{api_base_url}}/graph/clear | jq
