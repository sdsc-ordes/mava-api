import csv
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD

# Define your namespaces
MAVA = Namespace("http://example.org/mava/ontology#")
EX = Namespace("http://example.org/data/")

# 1. Initialize the graph and bind prefixes
g = Graph()
g.bind("mava", MAVA)
g.bind("ex", EX)

# Define the DataSeries this data belongs to
analysis_series = EX.MyAudioAnalysis
g.add((analysis_series, RDF.type, MAVA.DataSeries))
g.add((analysis_series, MAVA.seriesType, Literal("Voice Activity Score")))

# 2. Open and read the CSV
with open('input.csv', mode='r') as infile:
    reader = csv.DictReader(infile)
    for i, row in enumerate(reader):
        # 3. For each row, create resources and add triples
        start_time = row['startTime']
        numeric_value = row['value']

        # Create a unique URI for each data point
        data_point_uri = EX[f"point{i+1}"]

        # Add triples for the DataPoint
        g.add((data_point_uri, RDF.type, MAVA.DataPoint))
        g.add((data_point_uri, MAVA.atTime, Literal(start_time, datatype=XSD.decimal)))
        g.add((data_point_uri, MAVA.numericValue, Literal(numeric_value, datatype=XSD.decimal)))
        g.add((data_point_uri, MAVA.belongsToSeries, analysis_series))

# 4. Save the final graph to a Turtle file
with open("output.ttl", "w") as f:
    f.write(g.serialize(format="turtle"))

print("Transformation complete. Output saved to output.ttl")
