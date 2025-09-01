import csv
import io
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# Define namespaces here, close to the logic that uses them
MAVA = Namespace("http://example.org/mava/ontology#")
EX = Namespace("http://example.org/data/")


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

    def add_csv_data(self, csv_contents: str, filename: str):
        """Transforms CSV data and adds it to the graph."""
        csv_file = io.StringIO(csv_contents)
        reader = csv.DictReader(csv_file)

        # Create a unique series name from the CSV filename
        series_name = filename.split('.')[0]
        analysis_series = EX[series_name]
        self.g.add((analysis_series, RDF.type, MAVA.DataSeries))
        self.g.add((analysis_series, MAVA.seriesType, Literal("Voice Activity Score")))

        for i, row in enumerate(reader):
            start_time = row['startTime']
            numeric_value = row['value']
            data_point_uri = EX[f"{series_name}_point_{i+1}"]

            self.g.add((data_point_uri, RDF.type, MAVA.DataPoint))
            self.g.add((data_point_uri, MAVA.atTime, Literal(start_time, datatype=XSD.decimal)))
            self.g.add((data_point_uri, MAVA.numericValue, Literal(numeric_value, datatype=XSD.decimal)))
            self.g.add((data_point_uri, MAVA.belongsToSeries, analysis_series))

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
