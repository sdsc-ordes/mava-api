from typing import List, Dict
import pandas as pd
import io
import csv
from uuid import UUID
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

    def add_series(self, series_id: UUID, mapping: Dict, has_duration: bool):
        series_uri = EX[f"{series_id}"]

        series_description = mapping.get("series_description", None)
        value_description = mapping.get("value_description", None)

        # Set the series type
        if has_duration:
            self.g.add((series_uri, RDF.type, MAVA.AnnotationSeries))
        else:
            self.g.add((series_uri, RDF.type, MAVA.ObservationSeries))
        self.g.add((series_uri, MAVA.seriesDescription, Literal(series_description)))
        self.g.add((series_uri, MAVA.valueDescription, Literal(value_description)))

    def add_data(self, series_id: UUID, data: List[Dict], mapping: Dict, has_duration: bool):
        series_uri = EX[f"{series_id}"]

        # Get the required column names from the mapping
        time_key = mapping.get("time_column", None)
        value_key = mapping.get("value_column", None)
        value_type = mapping.get("value_type", None)
        duration_key = mapping.get("duration_column", None)

        # Process each data point
        for i, entry in enumerate(data):
            data_point_uri = EX[f"{series_id}_point_{i+1}"]
            self.g.add((data_point_uri, MAVA.belongsToSeries, series_uri))

            time_value = entry[time_key]
            value = entry[value_key]

            if has_duration:
                duration = entry[duration_key]
                self.g.add((data_point_uri, RDF.type, MAVA.AnnotationSegment))
                self.g.add((data_point_uri, MAVA.startTime, Literal(time_value, datatype=XSD.decimal)))
                self.g.add((data_point_uri, MAVA.endTime, Literal(time_value + duration, datatype=XSD.decimal)))
                self.g.add((data_point_uri, MAVA.stringValue, Literal(str(value), datatype=XSD.string)))
            else:
                self.g.add((data_point_uri, RDF.type, MAVA.ObservationPoint))
                self.g.add((data_point_uri, MAVA.atTime, Literal(time_value, datatype=XSD.decimal)))
                
                if value_type == "numeric":
                    self.g.add((data_point_uri, MAVA.numericValue, Literal(value, datatype=XSD.decimal)))
                elif value_type == "list":
                    self.g.add((data_point_uri, MAVA.listValue, Literal(str(value), datatype=RDF.List)))
    
    def add_mapped_data(
        self,
        data: List[Dict],
        mapping: Dict,
    ):
        """
        Validate and add data to the RDF graph based on a mapping of field names.

        Parameters:
        - data: List of dictionaries representing each row of tabular data.
        - mapping: Dictionary mapping field names to ontology properties.
        """

        validate_mapping(mapping=mapping, data=data)

        # Generate a unique series ID and add series information to the graph
        series_id = uuid.uuid4()
        duration_key = mapping.get("duration_key", None)
        has_duration = duration_key is not None
        self.add_series(series_id=series_id, mapping=mapping, has_duration=has_duration)

        # Add data instances to the graph
        self.add_data(series_id=series_id, data=data, mapping=mapping, has_duration=has_duration)


    def add_tsv_data(self, filename: str, mapping: dict):
        """
        Transforms tabular data (CSV or TSV) into RDF and adds it to the graph
        using a provided header-to-ontology mapping.
        """
        file_like_object = io.StringIO(filename)

        # Use pandas to read the data, automatically handling delimiters
        df = pd.read_csv(file_like_object, sep='\t')

        # Convert pandas dataframe to list of dictionaries
        data = df.to_dict(orient='records')
        self.add_mapped_data(data=data, mapping=mapping)

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
