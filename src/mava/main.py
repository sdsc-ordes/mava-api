from fastapi import FastAPI, Body, Response, HTTPException
from rdflib import Graph, URIRef
from rdflib.util import guess_format

# --- Global State ---
# This graph object will live in memory as long as the server is running.
# All API calls will interact with this single object.
g = Graph()


# --- FastAPI Application ---
app = FastAPI(
    title="Graph Builder API",
    description="An API to incrementally build and export an RDF graph.",
    version="1.0.0",
)


@app.get("/", summary="Check API status and graph size")
def read_root():
    """Returns the current status and the number of triples in the graph."""
    return {"status": "ok", "graph_size": len(g)}


@app.post("/graph/add", summary="Add RDF data to the graph")
def add_to_graph(
    content_type: str = "text/turtle",
    rdf_data: str = Body(..., media_type="text/plain")
):
    """
    Parses and adds new triples to the in-memory graph.
    The RDF data should be sent in the request body.
    """
    try:
        format = guess_format(content_type) or "turtle"
        g.parse(data=rdf_data, format=format)
        return {
            "message": "Data added successfully",
            "new_graph_size": len(g)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse RDF data: {e}")


@app.get("/graph/export", summary="Export the entire graph")
def export_graph(format: str = "turtle"):
    """
    Serializes and returns the entire graph in the specified format.
    Common formats: 'turtle', 'xml', 'json-ld', 'nt'.
    """
    if format not in ["turtle", "xml", "json-ld", "nt", "n3"]:
        raise HTTPException(status_code=400, detail="Invalid format requested.")

    return Response(
        content=g.serialize(format=format),
        media_type=f"application/rdf+{format}" if format == "xml" else f"text/{format}"
    )


@app.delete("/graph/clear", summary="Clear all triples from the graph")
def clear_graph():
    """Resets the graph to be empty."""
    global g
    g = Graph()
    return {"message": "Graph cleared successfully"}
