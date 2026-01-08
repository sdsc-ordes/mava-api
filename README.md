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

## Project Context

This work is part of the **MAVA Project**, which aims to improve
interoperability and data exchange among three research tools – _VideoScope_,
_TIB-AV-A_, and _VIAN_.

By standardizing data formats and developing shared APIs, the project enhances
data sharing and analysis capabilities across linguistic, media studies, and
audiovisual research.

This infrastructure will, for the first time, enable shared research workflows
and ensure adherence to _FAIR principles_, improving the accessibility and
reusability of research data.

## Installation

### Prerequisites

This repository relies on nix and direnv.

- Clone the github repo.
- `cd mava-api`
- `just build`
- `just run`

## PoC

This is a PoC, for a connector to achieve interoperability between video
metadata processing tools. It comes with the following building blocks:

- ontology for a common terminology
- api that allows to export and import into a graph that remains in memory.

### Ontology

- the ontology is provided in owl
- so far it has been kept pragmatic, aligned to the use cases TIBAV-A and
  videoscope

### API

- It establishes an API, that allows to import gradually into a graph and then
  exports the graph once it is ready
- The graph can also be cleared.
- Data can be imported from csv files or from Turtle files
- Data is exported as Turtle filed

## Development

Read first the [Contribution Guidelines](/CONTRIBUTING.md).

For technical documentation on setup and development, see the
[Development Guide](docs/development-guide.md)

## Acknowledgements

This work was funded by the Swiss Data Science Center (SDSC) through its
National Call for Projects as an Infrastructure project.

We gratefully acknowledge the contributions of the SDSC experts and our
partners.

**SDSC Experts**:

- Dr. Stefan Milosavljevic, ORCID ID
  [0000-0002-9135-1353](https://orcid.org/0000-0002-9135-1353)
- Sabine Maennel
- Robin Franken, ORCID ID
  [0009-0008-0143-9118](https://orcid.org/0009-0008-0143-9118)
- Dr. Oksana Riba Grognuz, ORCID ID
  [0000-0002-2961-2655](https://orcid.org/0000-0002-2961-2655)

**Partner Institutions**

- Dr. Teodora Vuković, ORCID ID
  [0000-0002-5780-5665](https://orcid.org/0000-0002-5780-5665)
- Dr. Jeremy Zehr, ORCID ID
  [0000-0002-6046-8647](https://orcid.org/0000-0002-6046-8647)
- Prof. Dr. Josephine Diecke, ORCID ID
  [0000-0002-9342-0631](https://orcid.org/0000-0002-9342-0631)
- Dr. Simon Spiegel, ORCID ID
  [0000-0003-2141-5566](https://orcid.org/0000-0003-2141-5566)
- Prof. Dr. Ralph Ewerth, ORCID ID
  [0000-0003-0918-6297](https://orcid.org/0000-0003-0918-6297)
- Dr. Eric Müller-Budack, ORCID ID
  [0000-0002-6802-1241](https://orcid.org/0000-0002-6802-1241)
- Dr. Cristina Grisot, ORCID ID
  [0000-0003-0684-4442](https://orcid.org/0000-0003-0684-4442)

## How to Cite

If you use this software, please cite it as follows:

👉 See the [CITATION.cff](./CITATION.cff) file for the full list of software
authors and citation formats.

When referring to the project more broadly (including partner contributions),
please acknowledge the funding statement and collaborators listed in the
[Acknowledgements](#acknowledgements) section:

> "This work was funded by the Swiss Data Science Center (SDSC) through its
> National Call for Projects as an Infrastructure project."

## Copyright

Copyright © 2025-2026 Swiss Data Science Center
(SDSC),[www.datascience.ch](http://www.datascience.ch/), ROR:
[ror.org/02hdt9m26](https://ror.org/02hdt9m26). All rights reserved. The SDSC is
a Swiss National Research Infrastructure, jointly established and legally
represented by the École Polytechnique Fédérale de Lausanne (EPFL) and the
Eidgenössische Technische Hochschule Zürich (ETH Zürich) as a société simple.
This copyright encompasses all materials, software, documentation, and other
content created and developed by the SDSC.
