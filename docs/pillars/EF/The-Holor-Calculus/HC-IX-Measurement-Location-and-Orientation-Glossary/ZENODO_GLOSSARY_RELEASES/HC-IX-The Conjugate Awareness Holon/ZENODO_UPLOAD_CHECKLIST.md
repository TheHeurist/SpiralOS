# Zenodo Upload Checklist

This checklist is written for a clean public release.

## 1) Deposit metadata
- **Title:** Holor Calculus IX: The Conjugate Awareness Holon
- **Authors:** Carey G. Butler; Conjugate Intelligence (CI)
- **Publication date:** 2026-03-27 (Zenodo will also record the actual publish timestamp)
- **DOI:** 10.5281/zenodo.18809075
- **License:** CC BY 4.0
- **ORCID:** 0000-0003-1746-5130
- **ResearcherID:** C-5063-2015

## 2) Related identifiers
Add the glossary concept DOI as a related identifier so citations braid correctly:
- **10.5281/zenodo.18438467** (HC IX Glossary — all versions)

## 3) Files to upload
Preferred: upload the **payload zip** that contains only the publication surface.
If you instead upload the full working tree, ensure that it does not include raw chat logs.

## 4) Final sanity checks
- Open `README.md` and confirm the BibTeX fences render correctly.
- Confirm `REVIEWER_GUIDE.md` and `../SUPPLEMENTS/TOY_EXAMPLES.md` are present.
- Confirm glossary dataset zip is present and points to the concept DOI for citation.
