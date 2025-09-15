# Build the documentation

docs_build_dir := "site"

# Lists all available 'docs' subcommands when 'just docs' is run
default:
    @just --list docs

# Meta-command to build the entire documentation site from scratch
[no-cd]
build: clean-site build-pylode build-openapi build-mkdocs build-root
    @echo ">> Documentation site successfully built in '{{docs_build_dir}}' directory."
    @echo ">> You can now serve the documentation using the following command:"
    @echo ">> uv run mkdocs serve -f docs/mkdocs.yml -a 127.0.0.1:8001"

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

# Copies the root index file to the final site directory
[no-cd]
build-root:
    @echo ">> Copying root index page..."
    @mkdir -p {{docs_build_dir}}
    @cp docs/root_index.html {{docs_build_dir}}/index.html
    @echo ">> Root index page available at {{docs_build_dir}}/index-html"

# Serves the documentation site with live reloading
[no-cd]
serve-mkdocs:
    @echo ">> Serving documentation at http://127.0.0.1:8001"
    uv run mkdocs serve -f docs/mkdocs.yml -a 127.0.0.1:8001

# Removes the old build directory
[no-cd]
clean-site:
    @echo ">> Cleaning old site directory...{{docs_build_dir}}"
    @rm -rf {{docs_build_dir}}
