# Build the documentation

docs_build_dir := "site"

# Meta-command to build the entire documentation site from scratch
docs-build-site: docs-clean-site docs-build-pylode docs-build-openapi docs-build-mkdocs docs-build-root
    @echo ">> Documentation site successfully built in '{{docs_build_dir}}' directory."
    @echo ">> You can now serve the documentation using the following command:"
    @echo ">> uv run mkdocs serve -f docs/mkdocs.yml -a 127.0.0.1:8001"

# Build the MkDocs site into the site/docs directory
docs-build-mkdocs:
    @echo ">> Building MkDocs site..."
    # The -d flag tells mkdocs where to put the output
    @uv run mkdocs build -f docs/mkdocs.yml -d ../{{docs_build_dir}}/docs

# Build the ontology documentation into the site/ontology directory
docs-build-pylode:
    @echo ">> Building ontology documentation..."
    @mkdir -p site/ontology
    @pylode src/ontology/mava.ttl -o site/ontology/index.html
    @echo ">> Ontology documentation available at docs/ontology/index.html"

# Generates the OpenAPI spec without running the server
docs-build-openapi:
    @echo ">> Generating OpenAPI specification..."
    uv run python tools/scripts/generate-spec.py

# Copies the root index file to the final site directory
docs-build-root:
    @echo ">> Copying root index page..."
    @mkdir -p {{docs_build_dir}}
    @cp docs/root_index.html {{docs_build_dir}}/index.html
    @echo ">> Root index page available at {{docs_build_dir}}/index-html"

# Serves the documentation site with live reloading
docs-serve-mkdocs:
    @echo ">> Serving documentation at http://127.0.0.1:8001"
    uv run mkdocs serve -f docs/mkdocs.yml -a 127.0.0.1:8001

# Removes the old build directory
docs-clean-site:
    @echo ">> Cleaning old site directory...{{docs_build_dir}}"
    @rm -rf {{docs_build_dir}}
