# Equine Assay Registry

The Equine Assay Registry is a collaborative database of immunoassays that have been tested for use in horses, including both successfully and unsuccessfully validated assays. This aims to improve transparency, reproducibility, and efficiency in equine research by reducing duplicated effort.

## Purpose

Relatively few immunoassays are developed specifically for equine applications, and research in horses often relies on assays designed for other species. Due to variable cross-species homology, identifying assays that perform reliably in equids can be time-consuming and resource-intensive. We propose to build a free, open, and collaborative repository of immunoassay validation data to facilitate equine research. Users can search for immunoassays and their validation outcomes in horses as well as submit validation data (both successful and unsuccessful).

## Contributing and Sharing Validation Data

### Types of contributions

- **Original validation data:** Information on an assay that has not been published before can be submitted using the submission form. Only authors can contribute original validation data. The contribution will be assigned a citable DOI.
- **Published validation data:** A submission submitted using the submission form can be linked to published works. This is comparable to registering a publication into the database, not to claiming authorship. Contributors are therefore not required to be the authors of the original work. This type of contribution will not be assigned a DOI.
- **Additions to existing entries:** Additional validation data or changes in assay information (e.g., assay has become unavailable) can be submitted from the entries found in the database. Contributors are required to be the authors of the additional validation data unless they reference published work. The information will be aggregated into a single entry tracking the different submissions.

### Attribution

- **Authors** refer to those who originally performed the assay validation. Authors can be contribute their data to the repository as contributors and be assigned a citable DOI if the work has not been previously published.
- **Contributors** are individuals who submit data to the registry. Anyone can contribute published works to the repository but they will not be attributed a DOI.

### Licensing

- All submitted data are shared under a **CC-BY 4.0 license**
- By submitting content, contributors agree to this license
- Contributors are responsible for ensuring that their submissions comply with any applicable licenses from original sources (e.g., published validation studies)

### Transparency and Review Process

- The submission process is fully open; all contributions are visible as GitHub issues
- Rejected submissions will include a documented justification

## Backend and Technical Framework

This project is designed to be extensible and adaptable to other domains.

- Data submission and versioning are managed via **GitHub**
- The frontend is deployed using **Vercel**
- The codebase is available under the **AGPL-3.0 license**

## Scope and Limitations

- The registry focuses on **immunoassays evaluated in equine samples**
- Validation quality and completeness depend on submitted data
- Inclusion in the registry does not constitute endorsement of assay performance

## Use of artificial intelligence (AI)

Microsoft Copilot was used to draft parts of the code in this repository. The
AI generated code snippets were tested and implemented manually by the author of
the repository.

