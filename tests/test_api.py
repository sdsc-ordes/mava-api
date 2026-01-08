import pytest
import json
from fastapi.testclient import TestClient
from mava.main import app
from mava.graph.builder import builder

# Create a TestClient instance based on your FastAPI app
client = TestClient(app)


# A pytest fixture to ensure the graph is clean before each test
@pytest.fixture(autouse=True)
def clean_graph_before_each_test():
    """Fixture to automatically clear the graph before every test."""
    builder.clear_graph()


def test_read_root():
    """Test the root endpoint to ensure it starts with an empty graph."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "graph_size": 0}


def test_add_to_graph():
    """Test adding a single triple via the raw RDF endpoint."""
    rdf_data = "@prefix mava: <http://example.org/mava/ontology#> . mava:Corpus1 a mava:Corpus ."
    response = client.post(
        "/graph/add", headers={"Content-Type": "text/turtle"}, content=rdf_data
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Data added successfully",
        "new_graph_size": 1,
    }

    # Verify the graph size with a subsequent call
    status_response = client.get("/")
    assert status_response.json()["graph_size"] == 1


def test_import_tsv():
    """
    Test uploading a TSV file with a custom mapping JSON.
    """
    # 1. Define the content of the TSV file
    tsv_content = (
        "start_in_seconds\tstart_hh:mm:ss.ms\tannotations\n"
        "0.0\t00:00:00.0\t0.11306\n"
        "0.5\t00:00:00.500\t0.11352\n"
        "1.0\t00:00:01.0\t0.16284\n"
        "1.5\t00:00:01.500\t0.18034\n"
        "2.0\t00:00:02.0\t0.18213\n"
    )

    # 2. Define the mapping and convert it to a JSON string
    mapping_data = {
        "series_description": "Cityview",
        "value_description": "probability for Cityview",
        "value_type": "numeric",
        "time_column": "start_in_seconds",
        "value_column": "annotations",
    }
    mapping_json_string = json.dumps(mapping_data)

    # 3. Simulate the multipart POST request with both the file and the mapping
    response = client.post(
        "/graph/import_tsv",
        # The 'files' parameter can send both file uploads and form fields
        files={
            "file": ("test.tsv", tsv_content, "text/tab-separated-values"),
            "mapping_json": (
                None,
                mapping_json_string,
            ),  # Send the mapping as a string field
        },
    )

    # 4. Assert the results
    assert response.status_code == 200
    assert response.json()["new_graph_size"] == 23


def test_export_graph():
    """Test that the export endpoint returns the added data."""
    # First, add some data to the graph
    rdf_data = "@prefix mava: <http://example.org/mava/ontology#> . mava:TestSubject a mava:TestClass ."
    # FIX: Added the required Content-Type header to the request.
    client.post("/graph/add", content=rdf_data, headers={"Content-Type": "text/turtle"})

    # Now, export it
    response = client.get("/graph/export")
    assert response.status_code == 200
    assert "mava:TestSubject" in response.text
    assert "mava:TestClass" in response.text


def test_clear_graph():
    """Test that the clear endpoint resets the graph."""
    # Add data
    rdf_data = "@prefix mava: <http://example.org/mava/ontology#> . mava:Corpus1 a mava:Corpus ."
    # FIX: Added the required Content-Type header to the request.
    client.post("/graph/add", content=rdf_data, headers={"Content-Type": "text/turtle"})

    # Verify it was added
    assert client.get("/").json()["graph_size"] == 1

    # Clear the graph
    response = client.delete("/graph/clear")
    assert response.status_code == 200
    assert response.json() == {"message": "Graph cleared successfully"}

    # Verify it's empty
    assert client.get("/").json()["graph_size"] == 0
