# ci commands

# Enter the default Nix development shell and execute the command `"$@`.
develop *args:
    just nix::develop "default" "$@"

# Format the project. Use --check to assess formatting.
format *args:
    @echo ">> Running formatter check (Ruff)..."
    nix run --accept-flake-config {{flake_dir}}#ruff -- format . "$@"

# Setup the project.
setup *args:
    cd "{{root_dir}}" && ./tools/scripts/setup.sh

# Run commands over the ci development shell.
ci *args:
    just nix::develop "ci" "$@"

# Lint the project.
lint *args:
    "{{root_dir}}/tools/scripts/setup-config-files.sh"
    nix run --accept-flake-config {{flake_dir}}#treefmt -- "$@"

# Run tests
test *args:
    @echo ">> Running tests...."
    # Set the PYTHONPATH to include the 'src' directory before running pytest
    PYTHONPATH=src pytest "$@"
