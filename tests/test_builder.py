import pytest
from mava.graph.builder import validate_mapping, GraphBuilder, MAVA, EX
from rdflib import Literal, RDF, XSD

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

@pytest.mark.parametrize("has_duration,value_type,expected_triples", [
    # Case 1: With duration
    (True, None, [
        (MAVA.startTime, Literal(10, datatype=XSD.decimal)),
        (MAVA.endTime, Literal(15, datatype=XSD.decimal)),
        (MAVA.stringValue, Literal("abc", datatype=XSD.string)),
    ]),
    # Case 2: Without duration, numeric value
    (False, "numeric", [
        (MAVA.atTime, Literal(10, datatype=XSD.decimal)),
        (MAVA.numericValue, Literal(42, datatype=XSD.decimal)),
    ]),
    # Case 3: Without duration, list value
    (False, "list", [
        (MAVA.atTime, Literal(10, datatype=XSD.decimal)),
        (MAVA.listValue, Literal(str([1, 2, 3]), datatype=RDF.List)),
    ]),
])
def test_add_data(mocker, has_duration, value_type, expected_triples):
    instance = GraphBuilder()
    instance.g = mocker.MagicMock()

    series_id = "fixed-uuid"
    data_point_idx = 1
    data_point_uri = EX[f"{series_id}_point_{data_point_idx}"]
    series_uri = EX[f"{series_id}"]

    data = [{"time": 10}]
    if has_duration:
        data[0].update({"value": "abc", "duration": 5})
    else:
        data[0]["value"] = 42 if value_type == "numeric" else [1, 2, 3]

    mapping = {
        "time_column": "time",
        "value_column": "value",
        "value_type": value_type,
        "duration_column": "duration" if has_duration else None,
    }

    instance.add_data(series_id, data, mapping, has_duration)

    expected = [
        mocker.call((data_point_uri, MAVA.belongsToSeries, series_uri)),
    ]

    if has_duration:
        expected.append(mocker.call((data_point_uri, RDF.type, MAVA.AnnotationSegment)))
    else:
        expected.append(mocker.call((data_point_uri, RDF.type, MAVA.ObservationPoint)))

    for pred, obj in expected_triples:
        expected.append(mocker.call((data_point_uri, pred, obj)))

    instance.g.add.assert_has_calls(expected)
    assert instance.g.add.call_count == len(expected)