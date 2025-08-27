set positional-arguments
set shell := ["bash", "-cue"]
root_dir := `git rev-parse --show-toplevel`
flake_dir := root_dir / "tools/nix"
output_dir := root_dir / ".output"
build_dir := output_dir / "build"

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
    ruff check
    just validate-ontology

# Build the project.
build *args:
    uv build --out-dir "{{build_dir}}" "$@"

# Build the ontology.
build-ontology *args:
    mkdir -p "{{build_dir}}/ontology"
    uv run build-ontology \
        "{{build_dir}}/ontology/enriched.ttl" "$@"

# Validate the ontology.
validate-ontology: build-ontology
    echo "Validating ontology..."
    uv run validate-ontology \
        src/ontology/mava.ttl \
        src/quality-checks/shacl-shacl.ttl

build-documentation:
    #!/usr/bin/env bash
    set -eu
    just build-ontology

    echo "Download 'shacl-play-cli' ..."
    mkdir -p "{{build_dir}}/shacl-play"
    curl -L https://github.com/sparna-git/shacl-play/releases/download/0.10.2/shacl-play-app-0.10.2-onejar.jar \
      --output "{{build_dir}}/shacl-play/cli.jar"

    echo "Run 'shacl-play-cli' ..."
    export GRAPHVIZ_DOT="$(which dot)"

    cd "{{build_dir}}/shacl-play"
    java -jar "cli.jar" \
        doc \
        -d \
        -i "{{build_dir}}/ontology/enriched.ttl" \
        -l en \
        -o "{{root_dir}}/docs/index.html"

# Test the project.
test *args:
    echo "TODO: Not implemented"

# Run an executable.
run *args:
    uv run cli "$@"

# Run the Jupyter notebook.
notebook *args:
    uv run python -m notebook "$@"
