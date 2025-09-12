set positional-arguments
set shell := ["bash", "-cue"]
root_dir := `git rev-parse --show-toplevel`
flake_dir := root_dir / "tools/nix"
output_dir := root_dir / ".output"
build_dir := output_dir / "build"

mod nix "./tools/just/nix.just"

# Build the project.
build *args:
    uv build --out-dir "{{build_dir}}" "$@"

# run mava server
run:
    uv run uvicorn src.mava.main:app --reload "$@"

# --- just commands to use the api ---
import './tools/just/ci.just'

# --- just commands to use the api ---
import './tools/just/test.just'

# --- just commands to use the api ---
import './tools/just/api.just'

# --- just commands to build and serve documentation ---
import './tools/just/docs.just'
