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
    uv run validate-ontology \
        "{{build_dir}}/ontology/enriched.ttl" \
        "src/ontology/mava.ttl" "$@"

# Test the project.
test *args:
    echo "TODO: Not implemented"

# Run an executable.
run *args:
    uv run cli "$@"

# Run the Jupyter notebook.
notebook *args:
    uv run python -m notebook "$@"
