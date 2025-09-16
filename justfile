set positional-arguments
set shell := ["bash", "-cue"]
root_dir := `git rev-parse --show-toplevel`
flake_dir := root_dir / "tools/nix"
output_dir := root_dir / ".output"
build_dir := output_dir / "build"

mod nix "./tools/just/nix.just"
mod api './tools/just/api.just'
mod docs './tools/just/docs.just'

# Default target if you do not specify a target.
default:
    just --list

# Build the project.
build *args:
    uv build --out-dir "{{build_dir}}" "$@"

# run mava server
run:
    uv run uvicorn src.mava.main:app --reload "$@"

# ci tasks
import './tools/just/ci.just'
