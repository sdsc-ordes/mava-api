from fastapi import FastAPI
from mava.api import graph

app = FastAPI(
    title="Graph Builder API",
    description="An API to incrementally build and export an RDF graph from various sources.",
    version="1.0.0",
)

# Include the routes from your graph.py file
app.include_router(graph.router)
