import json
from mava.main import app

# The main function to generate and save the spec
def generate_openapi_spec():
    """Generates the OpenAPI spec from the FastAPI app and saves it to a file."""
    print("Generating OpenAPI specification...")

    # Use the built-in method to get the schema as a dictionary
    openapi_schema = app.openapi()

    # Write the schema to a JSON file with nice formatting
    with open("openapi.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)

    print("Done. Specification saved to openapi.json")


if __name__ == "__main__":
    generate_openapi_spec()
