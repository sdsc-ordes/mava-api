# Concepts

The API can be used to gradually combine metadata on videos to build an in memory graph and then export it.

```mermaid
graph TD
    subgraph "Data Import / Building the Graph"
        A[<b>POST /graph/add</b><br/><i>Client sends raw RDF data</i>] --> C{In-Memory Graph};
        B[<b>POST /graph/import_tsv</b><br/><i>Client uploads a TSV file</i>] --> C{In-Memory Graph};
    end

    subgraph "Data Export & Management"
        C -- "Read/Serialize" --> D[<b>GET /graph/export</b><br/><i>Client downloads the graph</i>];
        E[<b>DELETE /graph/clear</b><br/><i>Client resets the graph</i>] -- "Modify/Reset" --> C;
    end

    style C fill:#cde4ff,stroke:#36c,stroke-width:2px;
```

## Import

The Graph can import arbitrary turtle files, to complement the graph for a video corpus with any metadata that is of value.

- `POST graph/import`: for adding custom turtle metadata to the graph.
- `POST graph/import_tsv`: for adding videoanalysis data to the graph (see for example [TIB-AV-A](tools.md#tib-av-a))

## Export

The graph can be exported as any time. You can always take a look on the current state of the graph. The export saves the graph to a turtle file.

- `GET graph/export`: for adding custom turtle metadata to the graph.

## Clear

The Graph will not be stored longterm, but only live during a MAVA session:

- `DELETE graph/clear`: there is an api route to clear the graph

<script src="https://hypothes.is/embed.js" async></script>
