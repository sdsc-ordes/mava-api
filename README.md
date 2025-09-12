<p align="center">
  <img src="./docs/assets/logo.svg" alt="project logo" width="250">
</p>

<h1 align="center">
  mava-api
</h1>
<p align="center">
</p>

[![Current Release](https://img.shields.io/github/release/sdsc-ordes/mava-api.svg?label=release)](https://github.com/sdsc-ordes/mava-api/releases/latest)
[![Pipeline Status](https://img.shields.io/github/actions/workflow/status/sdsc-ordes/mava-api/normal.yaml?label=ci)](https://github.com/sdsc-ordes/mava-api/actions/workflows/normal.yaml)
[![License label](https://img.shields.io/badge/License-Apache2.0-blue.svg?)](http://www.apache.org/licenses/LICENSE-2.0.html)

**Authors:**

- [Stefan Milosavljevic](mailto:stefan.milosavljevic@sdsc.ethz.ch)
- [Sabine Maennel](mailto:sabine.maennel@sdsc.ethz.ch)

## Installation

### Prerequisites
This repository relies on nix and direnv.
- Clone the github repo.
- `cd mava-api`
- `just build`
- `just run`

## PoC

This is a PoC, for a connector to achieve interoperability between video metadata processing tools. It comes with the following building blocks:

- ontology for a common terminology
- api that allows to export and import into a graph that remains in memory.


### Ontology

- the ontology is provided in owl
- so far it has been kept pragmatic, aligned to the use cases TIBAV-A and videoscope

### API
- It establishes an API, that allows to import gradually into a graph and then exports the graph once it is ready
- The graph can also be cleared.
- Data can be imported from csv files or from Turtle files
- Data is exported as Turtle filed

## Development

Read first the [Contribution Guidelines](/CONTRIBUTING.md).

For technical documentation on setup and development, see the
[Development Guide](docs/development-guide.md)

## Acknowledgement

This work was funded by the Swiss Data Science Center (SDSC) through its 
National Call for Projects as an Infrastructure project. We gratefully 
acknowledge the contributions of all project members and external collaborators.

## Copyright

Copyright © 2025-2028 Swiss Data Science Center (SDSC),
[www.datascience.ch](http://www.datascience.ch/). All rights reserved. 
The SDSC is a Swiss National Research Infrastructure, jointly established and legally represented 
by the École Polytechnique Fédérale de Lausanne (EPFL) and the Eidgenössische Technische Hochschule 
Zürich (ETH Zürich) as a société simple. This copyright encompasses all materials, software, 
documentation, and other content created and developed by the SDSC.
