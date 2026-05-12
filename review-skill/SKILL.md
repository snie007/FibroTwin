---
name: systematic-literature-review
description: Conduct rigorous, multi-agent systematic literature reviews with PRISMA-aligned methodology. Use when you need a comprehensive evidence synthesis with verified citations, structured findings tables, and clear prose narrative. Outputs include narrative summary (prose highlighting key findings), evidence tables (mapping claims to sources with PMIDs), and BibTeX bibliography with aggressive fact-checking by independent agent.
---

# Systematic Literature Review Skill

Produce high-quality literature reviews that are:
- **Structured**: Narrative prose + evidence tables + verified BibTeX
- **Verifiable**: Every claim traces to a specific source with PMID
- **Accurate**: Independent agent fact-checks all citations and findings
- **Relevant**: Focused on your specific research landscape (not generic Q&A lists)

## Quick Start

```
User Request: "Create a literature review on [TOPIC]"

Orchestrator delegates:
  1. Researcher Agent → Systematic search, data extraction, synthesis
  2. Verification Agent → Fact-check all claims, verify PMIDs, identify gaps
  3. Synthesis Agent → Integrate feedback, produce final narrative + tables

Output: 
  - narrative.md (prose highlighting main findings)
  - evidence_table.csv (claim → source mapping with PMIDs)
  - references.bib (BibTeX with verified citations)
```

## Workflow

### Phase 1: Scoping & Search Strategy (Researcher)

The researcher defines:

1. **Research Question**: What is the landscape/gap you're investigating?
   - Bad: "Tell me about digital twins"
   - Good: "What digital twins exist for lung disease modeling? What biological processes do they model? Are they mechanistic, data-driven, or hybrid?"

2. **Search Strategy**:
   - Define keywords and synonyms (e.g., "digital twin*", "virtual patient", "in silico model")
   - Identify 3–5 primary databases (PubMed, IEEE Xplore, arXiv, Web of Science)
   - Apply date range and language filters
   - Use Boolean operators to capture breadth without noise

3. **Inclusion/Exclusion Criteria**:
   - Include: peer-reviewed papers, preprints, clinical trials, FDA submissions
   - Exclude: editorials, opinion pieces, marketing materials, non-English (if specified)
   - Define population/intervention/outcome (PICO) if clinical context applies

4. **Data Extraction Form** (See references/extraction-template.md):
   - Study metadata (authors, year, venue, type)
   - Key findings (what was studied, results)
   - Biological processes modeled
   - Data sources (mechanistic, data-driven, hybrid?)
   - Clinical validation status
   - Limitations & gaps

### Phase 2: Screening & Quality Assessment

The researcher:

1. **Screen titles/abstracts** against inclusion criteria
2. **Full-text review** of promising studies
3. **Quality assessment** (See references/quality-checklist.md):
   - Is the method clearly described?
   - Are results validated (retrospective, prospective, clinical)?
   - Are limitations acknowledged?
   - Grade evidence as Strong/Moderate/Weak

### Phase 3: Data Synthesis & Narrative (Researcher + Synthesis Agent)

**Narrative Structure** (See references/narrative-template.md):

1. **Executive Summary**: Key findings at a glance (100–200 words)
2. **Current State**: Categorized overview of what exists (by process, scale, or clinical area)
3. **Novelty Gaps**: What's missing or understudied
4. **Clinical Translation Status**: How many systems deployed? Real-world validation?
5. **Synthesis by Research Question**: Answer each question with evidence-grounded narrative

**Evidence Table Structure** (CSV):

| Finding | Supporting Studies | PMID List | Evidence Grade | Notes |
|---------|-------------------|-----------|-----------------|-------|
| "Only 2–5 patient-specific twins deployed clinically" | inHEART (2024), Johns Hopkins VT trial, SOPHiA (2024) | 12345678, 87654321, ... | Strong | FDA clearance documented |
| "Most twins are data-driven for oncology" | Study A, Study B, Study C | ... | Moderate | Limited prospective validation |

### Phase 4: Verification & Quality Control (Verification Agent)

**Independent agent fact-checks**:

1. **Citation Verification**:
   - Does the PMID exist in PubMed?
   - Does the claim match what the paper actually says?
   - Flag misquotes, overstatements, missing context

2. **Completeness**:
   - Are all major studies captured?
   - Are there obvious gaps (recent papers, key researchers, major conferences)?
   - Suggest additional searches if warranted

3. **Bias Detection**:
   - Are positive findings over-represented?
   - Are critical studies included (papers showing limitations)?
   - Is the narrative balanced?

4. **Output**: Verification report identifying corrections needed; Researcher revises accordingly

### Phase 5: Final Synthesis (Synthesis Agent)

1. **Integrate verification feedback** into revised narrative and tables
2. **Generate BibTeX** with verified metadata (author, title, year, venue, PMID, DOI, URL)
3. **Validate formatting**: All references cited in prose appear in bibliography; no orphaned references
4. **Final QA**: Proof narrative for clarity, check tables for consistency

## Deliverables

### 1. narrative.md
Prose-focused synthesis (~2000–4000 words) organized by research question:

```
# Literature Review: Digital Twins in Lung Disease

## Executive Summary
[Key findings in 100–200 words]

## Current State: Digital Twin Landscapes
### Mechanistic Twins (Physics-Based)
- Description of approaches
- Examples from literature
- Limitations

### Data-Driven Twins (ML-Based)
- Description of approaches
- Examples from literature
- Limitations

### Hybrid Twins
- Description of approaches
- Examples from literature
- Strengths and gaps

## Biological Processes Modeled
[Organized by process: tumor growth, immune infiltration, drug metabolism, etc.]

## Clinical Translation & Validation
[Summary of deployed systems, evidence grades, prospective vs. retrospective]

## Novelty Gaps
[Clear articulation of what's missing, opportunities for innovation]

## References
[Full BibTeX-style citations]
```

### 2. evidence_table.csv
Structured claim-to-source mapping:

```csv
Claim,Studies,PMIDs,Evidence_Grade,Confidence,Notes
"Only 2–5 patient-specific digital twins have clinical FDA clearance",inHEART 2024; Johns Hopkins 2023; SOPHIA GENETICS 2024,12345678; 87654321; 11111111,Strong,High,"inHEART cardiac ablation (510k approved March 2024); Johns Hopkins VT trial active; SOPHIA launched Oct 2024"
"Mechanistic twins for cardiac are most mature",Duke cardiology labs; Mayo Clinic; Siemens,,,,"Multiple prospective trials; FDA pathway clear"
"Oncology twins mostly data-driven",Smith et al 2024; Jones et al 2023,22222222; 33333333,Moderate,Medium,"Few mechanistic tumor models clinically validated; most use ML on imaging+genomics"
```

### 3. references.bib
BibTeX bibliography (verified PMIDs + DOIs):

```bibtex
@article{smith2024digital,
  title={Digital Twins in Precision Oncology},
  author={Smith, J. and Jones, K.},
  journal={Nature Medicine},
  year={2024},
  volume={30},
  number={3},
  pages={456-468},
  doi={10.1038/s41591-024-01234-x},
  pmid={12345678},
  note={FDA pathway review}
}

@inproceedings{jones2023cardiac,
  title={Patient-Specific Cardiac Digital Twins for Arrhythmia Prediction},
  author={Jones, K. and Brown, L.},
  booktitle={IEEE EMBC Conference},
  year={2023},
  pages={1234-1240},
  pmid={87654321}
}
```

## Multi-Agent Orchestration

**You (Orchestrator) manage the workflow**:

1. **Spawn Researcher Agent**:
   ```
   Task: Systematic search for [TOPIC]. 
   Define research questions. Extract data from [N] top sources.
   Output: findings.md with structured data.
   ```

2. **Spawn Verification Agent**:
   ```
   Task: Fact-check all findings from researcher.
   Verify each PMID exists and matches claims.
   Flag overstatements or missing context.
   Output: verification_report.md with corrections.
   ```

3. **Integrate & Synthesize**:
   - Read both reports
   - Merge findings with corrections
   - Generate final narrative + evidence table + BibTeX
   - Proofread for clarity and consistency

## References for This Skill

- See references/extraction-template.md for data extraction form
- See references/quality-checklist.md for quality assessment framework
- See references/narrative-template.md for narrative structure examples
- See references/prisma-checklist.md for PRISMA 2020 compliance items

## Key Principles

1. **Every claim must have a source** — If you can't cite it, remove it
2. **PMIDs are non-negotiable** — Verification agent checks each one
3. **Narrative first, then evidence** — Prose tells the story; tables support it
4. **No orphaned questions** — Don't list Q&A; synthesize into findings
5. **Acknowledge limitations** — What wasn't covered? What's uncertain?

## Common Mistakes to Avoid

- ✗ Long lists of bullet-point summaries (no narrative synthesis)
- ✗ Claims without sources
- ✗ Wrong or missing PMIDs
- ✗ Assuming reviewer knows the field (explain jargon briefly)
- ✗ Ignoring contradictory findings (include them; explain discrepancies)
- ✗ Missing recent papers (search 2023–present)
- ✗ No clarity on clinical vs. research twin status

## Tips for Accuracy

1. **Use PubMed directly**: Verify every PMID before including it
2. **Cross-check claims**: If Study A says X and Study B says not-X, explain the discrepancy
3. **Grade evidence explicitly**: Distinguish between Strong (RCTs, FDA data), Moderate (cohort studies), Weak (case reports, models)
4. **Be transparent about gaps**: "This review focuses on [scope]; we did not include [reasons]"
5. **Engage external verification**: Have an independent agent challenge your claims

## When to Use This Skill

- ✓ Grant applications requiring literature background
- ✓ Addressing reviewer comments about novelty
- ✓ Scoping a new research area
- ✓ Comparing competing approaches (mechanistic vs. data-driven)
- ✓ Identifying clinical translation barriers
- ✗ NOT for: writing opinion pieces, summarizing a single paper, answering quick Q&A

## Outputs Beyond the PDF

- **narrative.md**: Use as background for proposal revisions
- **evidence_table.csv**: Reference when reviewers challenge specific claims
- **references.bib**: Import directly into Overleaf or other LaTeX editors
- **verification_report.md**: Review corrections; understand where literature has gaps
