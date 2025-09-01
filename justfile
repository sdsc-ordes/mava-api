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
site_dir := "site"

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

# Removes the old build directory
clean-site:
    @echo ">> Cleaning old site directory..."
    @rm -rf {{site_dir}}

# Build the ontology documentation into the site/ontology directory
build-ontology-docs:
    @echo ">> Building ontology documentation..."
    @mkdir -p {{site_dir}}/ontology
    @pylode src/ontology/mava.ttl -o {{site_dir}}/ontology/index.html 2> /dev/null

# Build the MkDocs site into the site/docs directory
build-mkdocs:
    @echo ">> Building MkDocs site..."
    # The -d flag tells mkdocs where to put the output
    @uv run mkdocs build -f docs/mkdocs.yml -d {{site_dir}}/docs

# Copies the root index file to the final site directory
build-root-index:
    @echo ">> Creating root index page..."
    @cp docs/root_index.html {{site_dir}}/index.html

# Meta-command to build the entire documentation site from scratch
build-site: clean-site build-ontology-docs build-mkdocs build-root-index
    @echo ">> Documentation site successfully built in '{{site_dir}}' directory."
    @echo ">> You can now serve the documentation using the following command:"
    @echo ">> uv run mkdocs serve -f docs/mkdocs.yml -a 127.0.0.1:8001"