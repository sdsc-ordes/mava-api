# MAVA Ontology

The MAVA Ontology is just a Draft for now and will be revised later on.

## Guiding Principles

- establish the ontology in owl
. start with the basic vocabulary that the tools need to describe their metadata
. complexity and alingment with existing vocabularies can be acchieved later on

## Pylode Documentation

The ontology is documented with [pylode](https://github.com/RDFLib/pyLODE).

[MAVA-Ontology Documentation](https://sdsc-ordes.github.io/mava-api/ontology/){ .md-button }

## Classes

Below you can see the current class diagram:

- **Video**: links the analyis together (as MAVA connects metadata on videos)
- **DataSeries**: TIB AV-A provides some analysis as data series, with measurements at certain timepoints
- **TImelines**: text annotations for example come as timelines, annotating for time intervals rather then for data points

```mermaid
classDiagram
    direction TB

    class VideoCorpus {
        +hasMember(Video)
    }

    class Video {
        +hasTimeline(Timeline)
    }

    class Timeline {
        +hasSegment(Segment)
    }

    class Segment {
        +startTime: decimal
        +endTime: decimal
        +hasAnnotation(Annotation)
    }

    class Annotation {
        +hasTextValue: string
    }

    class DataSeries {
        +seriesType: string
        +describesResource(Video)
    }

    class DataPoint {
        +atTime: decimal
        +numericValue: decimal
        +belongsToSeries(DataSeries)
    }

    note for Video "Central class linking different types of analysis"

    VideoCorpus --o Video : hasMember
    Video --> Timeline : hasTimeline
    Timeline --> Segment : hasSegment
    Segment --> Annotation : hasAnnotation

    DataSeries ..> Video : describesResource
    DataPoint ..> DataSeries : belongsToSeries
```

## Timeline

```mermaid
graph LR
    A[Video] -->|hasTimeline| B(Timeline)
    B -->|hasSegment| C(Segment)
    C -->|hasAnnotation| D(Annotation)
```

**Segment**: represents a Duration:

- startTime: 10.5s
- endTime: 15.2s
- Annotation: "Sone annotation on the time inteval in the video"

## DataSeries

```mermaid
graph LR
    E[Video]
    F(DataSeries) -->|describesResource| E
    G(DataPoint) -->|belongsToSeries| F
```

**Data Point**: represents an Instant and a Measurement:

- atTime: 1.75s
- numericValue: 0.883
