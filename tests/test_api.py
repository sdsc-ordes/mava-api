import pytest
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
    yield # This is where the test runs

def test_read_root():
    """Test the root endpoint to ensure it starts with an empty graph."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "graph_size": 0}

def test_add_to_graph():
    """Test adding a single triple via the raw RDF endpoint."""
    rdf_data = '@prefix mava: <http://example.org/mava/ontology#> . mava:Corpus1 a mava:Corpus .'
    response = client.post(
        "/graph/add",
        headers={"Content-Type": "text/turtle"},
        content=rdf_data
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Data added successfully", "new_graph_size": 1}

    # Verify the graph size with a subsequent call
    status_response = client.get("/")
    assert status_response.json()["graph_size"] == 1

def test_import_csv():
    """Test uploading and processing a CSV file."""
    csv_content = "startTime,value\n1.75,0.88385\n5.75,0.65886"

    # The 'files' parameter simulates a file upload
    response = client.post(
        "/graph/import_csv",
        files={"file": ("test.csv", csv_content, "text/csv")}
    )
    assert response.status_code == 200
    # FIX: The expected size was incorrect. It should be 10.
    # 2 triples for the DataSeries + (4 triples * 2 rows) = 10.
    assert response.json()["new_graph_size"] == 10

def test_export_graph():
    """Test that the export endpoint returns the added data."""
    # First, add some data to the graph
    rdf_data = '@prefix mava: <http://example.org/mava/ontology#> . mava:TestSubject a mava:TestClass .'
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
    rdf_data = '@prefix mava: <http://example.org/mava/ontology#> . mava:Corpus1 a mava:Corpus .'
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
