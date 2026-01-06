from typing import List, Dict, Optional
import pandas as pd
import io
import csv
import uuid
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# Define namespaces here, close to the logic that uses them
MAVA = Namespace("http://example.org/mava/ontology#")
EX = Namespace("http://example.org/data/")

def validate_mapping(mapping: dict, data: List[Dict]):
    """
    Validates that the dictionary-based mapping and data contain the required keys for time and value columns.
    If either is missing, a `ValueError` is raised.
    """
    time_key = mapping.get("time_column")
    value_key = mapping.get("value_column")

    if not time_key or not value_key:
        raise ValueError("Mapping must include 'time_column' and 'value_column' keys.")
    if any(time_key not in entry or value_key not in entry for entry in data):
        raise ValueError(f"Required keys '{time_key}' or '{value_key}' missing in some data entries.")
    

class GraphBuilder:
    """A service class to manage the in-memory RDF graph."""
    def __init__(self):
        self.g = Graph()
        self.g.bind("mava", MAVA)
        self.g.bind("ex", EX)

    def get_size(self) -> int:
        """Returns the current number of triples in the graph."""
        return len(self.g)

    def add_rdf_data(self, rdf_data: str, format: str = "turtle"):
        """Parses and adds new triples to the graph from a raw string."""
        self.g.parse(data=rdf_data, format=format)

    def add_series(self, has_duration: bool):
        # Generate a unique series ID
        series_id = uuid.uuid4()
        series_uri = EX[f"{series_id}"]

        # Set the series type
        if has_duration:
            self.g.add((series_uri, RDF.type, MAVA.AnnotationSeries))
        else:
            self.g.add((series_uri, RDF.type, MAVA.ObservationSeries))
    
    def add_mapped_data(
        self,
        data: List[Dict],
        mapping: Dict,
        series_description: str,
        value_description: str,
        value_type: str,
        duration_key: Optional[str] = None
    ):
        """
        Adds data to the RDF graph based on a mapping of field names.

        Parameters:
        - data: List of dictionaries representing each row of tabular data.
        - mapping: Dictionary mapping field names to ontology properties.
        - series_description: Description of the series.
        - value_description: Description of the values in the series.
        - value_type: Type of the value ("numeric", "list", etc.).
        - duration_key: Optional key indicating a duration field.
        """


    def add_tsv_data(self, data_contents: str, filename: str, mapping: dict):
        """
        Transforms tabular data (CSV or TSV) into RDF and adds it to the graph
        using a provided header-to-ontology mapping.
        """
        file_like_object = io.StringIO(data_contents)

        # Use pandas to read the data, automatically handling delimiters
        df = pd.read_csv(file_like_object, sep='\t')

        # Get the required column names from the mapping
        time_col = mapping.get("time_column", None)
        value_col = mapping.get("value_column", None)
        series_description = mapping.get("series_description", None)
        value_description = mapping.get("value_description", None)
        value_type = mapping.get("value_type", None)
        duration_col = mapping.get("duration_column", None)

        if not time_col or not value_col:
            raise ValueError("Mapping must include 'time_column' and 'value_column' keys.")

        if time_col not in df.columns or value_col not in df.columns:
            raise ValueError(f"Mapping columns '{time_col}' or '{value_col}' not found in file.")

        # Create a unique series name from the filename
        series_id = uuid.uuid4()
        series_uri = EX[f"{series_id}"]
        has_duration = duration_col and duration_col in df.columns
        if has_duration:
            self.g.add((series_uri, RDF.type, MAVA.AnnotationSeries))
        else:
            self.g.add((series_uri, RDF.type, MAVA.ObservationSeries))
        self.g.add((series_uri, MAVA.seriesDescription, Literal(series_description)))
        self.g.add((series_uri, MAVA.valueDescription, Literal(value_description)))

        # Loop through the DataFrame rows
        for i, row in df.iterrows():
            start_time = row[time_col]
            duration = row[duration_col] if has_duration else 0
            value = row[value_col]

            data_point_uri = EX[f"{series_id}_point_{i+1}"]
            self.g.add((data_point_uri, MAVA.belongsToSeries, series_uri))
            if has_duration:
                duration = row[duration_col]
                self.g.add((data_point_uri, RDF.type, MAVA.AnnotationSegment))
                self.g.add((data_point_uri, MAVA.startTime, Literal(start_time, datatype=XSD.decimal)))
                self.g.add((data_point_uri, MAVA.endTime, Literal(start_time + duration, datatype=XSD.decimal)))
                self.g.add((data_point_uri, MAVA.stringValue, Literal(value, datatype=XSD.string)))
            else:
                self.g.add((data_point_uri, RDF.type, MAVA.ObservationPoint))
                self.g.add((data_point_uri, MAVA.atTime, Literal(start_time, datatype=XSD.decimal)))
                self.g.add((data_point_uri, MAVA.belongsToSeries, series_uri))
                if value_type == "numeric":
                    self.g.add((data_point_uri, MAVA.numericValue, Literal(value, datatype=XSD.decimal)))
                elif value_type == "list":
                    self.g.add((data_point_uri, MAVA.listValue, Literal(value, datatype=RDF.List)))

    def export_graph(self, format: str = "turtle") -> bytes:
        """Serializes the entire graph to the specified format."""
        return self.g.serialize(format=format)

    def clear_graph(self):
        """Resets the graph to an empty state."""
        self.g = Graph()
        self.g.bind("mava", MAVA)
        self.g.bind("ex", EX)


# Create a single, shared instance of the builder.
# This "singleton" will hold the graph state for the application's lifetime.
builder = GraphBuilder()
