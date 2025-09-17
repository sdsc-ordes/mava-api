# Build the documentation

docs_build_dir := "site"

# Lists all available 'docs' subcommands when 'just docs' is run
default:
    @echo ">>List just commands for docs"
    @just --list docs

# Meta-command to build the entire documentation site from scratch
[no-cd]
build: clean-site build-pylode build-openapi build-mkdocs
    @echo ">> Documentation site successfully built in '{{docs_build_dir}}' directory."

# Build the MkDocs site into the site/docs directory
[no-cd]
build-mkdocs:
    @echo ">> Building MkDocs site..."
    # The -d flag tells mkdocs where to put the output
    @uv run mkdocs build -f docs/mkdocs.yml -d ../{{docs_build_dir}}/docs

# Build the ontology documentation into the site/ontology directory
[no-cd]
build-pylode:
    @echo ">> Building ontology documentation..."
    @mkdir -p {{docs_build_dir}}/ontology
    @pylode src/ontology/mava.ttl -o {{docs_build_dir}}/ontology/index.html
    @echo ">> Ontology documentation available at {{docs_build_dir}}/ontology/index.html"

# Generates the OpenAPI spec without running the server
[no-cd]
build-openapi:
    @echo ">> Generating OpenAPI specification..."
    uv run python tools/scripts/generate-spec.py

# Serves the documentation site with live reloading
[no-cd]
serve:
    @echo ">> Serving documentation..."
    uv run mkdocs serve -f docs/mkdocs.yml -a 127.0.0.1:8001

# Removes the old build directory
[no-cd]
clean-site:
    @echo ">> Cleaning old site directory...{{docs_build_dir}}"
    @rm -rf {{docs_build_dir}}
