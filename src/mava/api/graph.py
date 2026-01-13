from fastapi import APIRouter, Body, Response, HTTPException, UploadFile, File, Form
from mava.graph.builder import builder
import json

# Create an APIRouter instance
router = APIRouter()


@router.get("/", summary="Check API status and graph size")
def read_root():
    """Returns the current status and the number of triples in the graph."""
    return {"status": "ok", "graph_size": builder.get_size()}


@router.post("/graph/add", summary="Add Turtle data to the graph")
def add_to_graph(rdf_data: str = Body(..., media_type="text/plain")):
    """Parses and adds new triples to the in-memory graph."""
    try:
        builder.add_rdf_data(rdf_data)
        return {
            "message": "Data added successfully",
            "new_graph_size": builder.get_size(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse RDF data: {e}")


@router.post("/graph/import_tsv", summary="Import data from a TSV file")
async def import_tsv(file: UploadFile = File(...), mapping_json: str = Form(...)):
    """
    Accepts a tsv file upload (TSV), transforms it to RDF
    using a JSON mapping, and adds it to the graph.
    """
    try:
        # The 'format' query parameter is no longer needed
        mapping = json.loads(mapping_json)
        contents = await file.read()

        # Update this function call to remove the delimiter
        builder.add_tsv_data(
            data_contents=contents.decode("utf-8"),
            filename=file.filename,
            mapping=mapping,
        )
        return {
            "message": f"Successfully imported data from {file.filename}",
            "new_graph_size": builder.get_size(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process file: {e}")


@router.get("/graph/export", summary="Export the entire graph")
def export_graph(format: str = "turtle"):
    """Serializes and returns the entire graph in the specified format."""
    if format not in ["turtle", "xml", "json-ld", "nt", "n3"]:
        raise HTTPException(status_code=400, detail="Invalid format requested.")

    content = builder.export_graph(format=format)
    media_type = f"application/rdf+{format}" if format == "xml" else f"text/{format}"
    return Response(content=content, media_type=media_type)


@router.delete("/graph/clear", summary="Clear all triples from the graph")
def clear_graph():
    """Resets the graph to be empty."""
    builder.clear_graph()
    return {"message": "Graph cleared successfully"}
