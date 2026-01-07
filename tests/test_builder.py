import pytest
from mava.graph.builder import validate_mapping, GraphBuilder, MAVA, EX
from rdflib import URIRef, Literal, RDF

def test_validate_mapping_valid():
    mapping = {"time_column": "t", "value_column": "v"}
    data = [{"t": 1, "v": 2}]
    validate_mapping(mapping, data)

def test_validate_mapping_missing_keys():
    mapping = {"time_column": "t"}
    data = [{"t": 1, "v": 2}]
    with pytest.raises(ValueError, match="Mapping must include 'time_column' and 'value_column' keys"):
        validate_mapping(mapping, data)

def test_validate_mapping_missing_in_data():
    mapping = {"time_column": "t", "value_column": "v"}
    data = [{"t": 1}]  # Missing 'v'
    with pytest.raises(ValueError, match="Required keys 't' or 'v' missing in some data entries"):
        validate_mapping(mapping, data)

@pytest.mark.parametrize("has_duration,expected_type", [
    (True, "AnnotationSeries"),
    (False, "ObservationSeries"),
])
def test_add_series(mocker, has_duration, expected_type):
    instance = GraphBuilder()
    instance.g = mocker.MagicMock()

    series_id = "fixed-uuid"
    mapping = {
        "series_description": "Test Series",
        "value_description": "Test Value",
    }

    instance.add_series(series_id, mapping, has_duration)

    series_uri = EX[f"{series_id}"]
    type_triple = (series_uri, RDF.type, getattr(MAVA, expected_type))
    description_triple = (series_uri, MAVA.seriesDescription, Literal("Test Series"))
    value_desc_triple = (series_uri, MAVA.valueDescription, Literal("Test Value"))

    calls = [
        mocker.call(type_triple),
        mocker.call(description_triple),
        mocker.call(value_desc_triple),
    ]
    instance.g.add.assert_has_calls(calls)
    instance.g.add.call_count == 3