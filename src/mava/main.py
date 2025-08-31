import csv
import io
from fastapi import FastAPI, Body, Response, HTTPException, UploadFile, File
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD

# --- Global State ---
# This graph object will live in memory as long as the server is running.
# All API calls will interact with this single object.
g = Graph()
MAVA = Namespace("http://example.org/mava/ontology#")
EX = Namespace("http://example.org/data/")
g.bind("mava", MAVA)
g.bind("ex", EX)


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
        format = "turtle"
        g.parse(data=rdf_data, format=format)
        return {
            "message": "Data added successfully",
            "new_graph_size": len(g)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse RDF data: {e}")

@app.post("/graph/import_csv", summary="Import data from a CSV file")
async def import_csv(file: UploadFile = File(...)):
    """
    Accepts a CSV file upload, transforms it to RDF, and adds it to the graph.
    Expects CSV with columns: 'startTime', 'value'
    """
    try:
        # Read the uploaded file content as bytes
        contents = await file.read()
        # Decode bytes to a string and treat it like a file for the csv reader
        csv_file = io.StringIO(contents.decode("utf-8"))
        reader = csv.DictReader(csv_file)

        # Define the DataSeries this data belongs to
        analysis_series = EX.MyAudioAnalysis
        g.add((analysis_series, RDF.type, MAVA.DataSeries))
        g.add((analysis_series, MAVA.seriesType, Literal("Voice Activity Score")))

        # Loop through CSV rows and create triples
        for i, row in enumerate(reader):
            start_time = row['startTime']
            numeric_value = row['value']
            data_point_uri = EX[f"point_csv_{i+1}"]

            g.add((data_point_uri, RDF.type, MAVA.DataPoint))
            g.add((data_point_uri, MAVA.atTime, Literal(start_time, datatype=XSD.decimal)))
            g.add((data_point_uri, MAVA.numericValue, Literal(numeric_value, datatype=XSD.decimal)))
            g.add((data_point_uri, MAVA.belongsToSeries, analysis_series))

        return {
            "message": f"Successfully imported data from {file.filename}",
            "new_graph_size": len(g)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process CSV file: {e}")

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
