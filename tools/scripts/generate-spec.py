import json
import yaml
import os
from mava.main import app

# The main function to generate and save the spec
def generate_openapi_spec():
    """Generates the OpenAPI spec from the FastAPI app and saves it to a file."""
    print("Generating OpenAPI specification...")

 # Define the output path inside the 'docs' directory
    output_path = "docs/mkdocs/openapi.yaml"
    output_dir = os.path.dirname(output_path)

    # Ensure the output directory exists before writing the file
    os.makedirs(output_dir, exist_ok=True)

    # Use the built-in method to get the schema as a dictionary
    openapi_schema = app.openapi()

    # Write the schema to a YAML file with nice formatting
    with open(output_path, "w") as f:
        yaml.dump(openapi_schema, f, indent=2, sort_keys=False)

    print("Done. Specification saved to docs/mkdocs/openapi.yaml")


if __name__ == "__main__":
    generate_openapi_spec()
