# Test the project.

# Run tests
test *args:
    @echo ">> Running tests...."
    # Set the PYTHONPATH to include the 'src' directory before running pytest
    PYTHONPATH=src pytest "$@"
