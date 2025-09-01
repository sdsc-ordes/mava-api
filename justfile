set positional-arguments
set shell := ["bash", "-cue"]
root_dir := `git rev-parse --show-toplevel`
flake_dir := root_dir / "tools/nix"
output_dir := root_dir / ".output"
build_dir := output_dir / "build"
api_base_url := "http://localhost:8000"
default_import_file := "examples/input/input.ttl"
default_export_file := "examples/output/export.ttl"
default_csv_file := "examples/input/input.csv"

mod nix "./tools/just/nix.just"

# Default target if you do not specify a target.
default:
    just --list --unsorted

# Enter the default Nix development shell and execute the command `"$@`.
develop *args:
    just nix::develop "default" "$@"

# Format the project.
format *args:
    "{{root_dir}}/tools/scripts/setup-config-files.sh"
    nix run --accept-flake-config {{flake_dir}}#treefmt -- "$@"

# Setup the project.
setup *args:
    cd "{{root_dir}}" && ./tools/scripts/setup.sh

# Run commands over the ci development shell.
ci *args:
    just nix::develop "ci" "$@"

# Lint the project.
lint *args:
    echo "TODO: Not implemented"

# Build the project.
build *args:
    uv build --out-dir "{{build_dir}}" "$@"

# run mava server
run:
    uv run uvicorn src.mava.main:app --reload "$@"

# Build the documentation.
build-ontology-docs:
    @echo ">> Building documentation..."
    pylode src/ontology/mava.ttl -o docs/index.html 2> /dev/null
    @echo ">> Building documentation complete at docs/index.html."

# Generates the OpenAPI spec without running the server
build-openapi-docs:
    @echo ">> Generating OpenAPI specification..."
    uv run python tools/scripts/generate-spec.py

# Test the project.
test *args:
    @echo ">> Running tests...."
    # Set the PYTHONPATH to include the 'src' directory before running pytest
    PYTHONPATH=src pytest "$@"

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


# Imports data from a specified CSV file (defaults to input.csv)
import-csv filename=default_csv_file:
    @echo ">> Importing data from CSV file '{{filename}}'..."
    @curl -sS -X POST {{api_base_url}}/graph/import_csv \
        -F "file=@{{filename}};type=text/csv" | jq


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

# --- Documentation (MkDocs) ---

# Serves the documentation site locally for development
docs-serve:
    @echo ">> Serving documentation at http://127.0.0.1:8001"
    uv run mkdocs serve -f docs/mkdocs.yml -a 127.0.0.1:8001

# Builds the static documentation site
docs-build:
    @echo ">> Building documentation site..."
    uv run mkdocs build -f docs/mkdocs.yml

# Build all documentation source files (Ontology, OpenAPI)
build-all-docs: build-ontology-docs build-openapi-docs