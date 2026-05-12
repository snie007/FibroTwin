# Narrative Writing Template for Literature Reviews

Use this structure to write prose that tells a coherent story, not a Q&A list.

## Narrative Structure

### 1. Executive Summary (100–200 words)

**Purpose**: Reader gets the key takeaway without reading further.

**Structure**:
- Opening: What landscape are we looking at?
- Current state: What dominates (numerically or conceptually)?
- Gap: What's missing?
- Implication: Why does this matter?

**Example**:
> Digital twins for cardiac electrophysiology have achieved the furthest clinical translation, with FDA-cleared systems (inHEART, 2024) now guiding ablation procedures. However, twins for oncology remain in research phase, with most systems using data-driven approaches (ML on imaging + genomics) rather than mechanistic models. A major gap is multi-scale integration—current twins model single processes (tumor growth OR immune response) but not both simultaneously. This review examines 47 studies across cardiac, oncology, and emerging tissue-engineering domains, finding that clinical deployment requires not just accurate models but standardized data assimilation, regulatory frameworks, and prospective validation. We identify five key novelty gaps where new research could accelerate translation.

### 2. Current State (2000–3000 words)

**Purpose**: Establish what exists, organized by category (not by paper).

**Structure** (pick one organizing principle):

#### Option A: By Modeling Approach
- **Mechanistic (Physics-Based) Twins**
  - What they are
  - Where deployed (examples from literature)
  - Strengths & limitations
  - Biological processes best suited
  
- **Data-Driven (ML) Twins**
  - What they are
  - Where deployed (examples from literature)
  - Strengths & limitations
  - Data requirements
  
- **Hybrid Twins**
  - What they are
  - Where deployed (examples from literature)
  - How they combine mechanistic + ML
  - Emerging promise

#### Option B: By Biological System
- **Cardiac Electrophysiology**
  - Clinical status (most mature)
  - Example systems (inHEART, Johns Hopkins, Duke)
  - Validation evidence
  - Limitations
  
- **Oncology**
  - Clinical status (research phase)
  - Example systems (SOPHiA GENETICS, etc.)
  - Validation evidence
  - Data challenges

#### Option C: By Clinical Translation Stage
- **Research-Only Twins**
  - Characteristics
  - Examples
  - Why not clinical yet?
  
- **Clinical Trials / Early Deployment**
  - Characteristics
  - Examples
  - Validation approach
  
- **FDA-Cleared / Clinical Deployment**
  - Characteristics
  - Examples
  - Regulatory pathway

**Within each section**:
1. **Opening**: What's the state of the art here?
2. **Examples**: Cite 2–4 key studies showing the landscape
3. **Methods**: What approaches dominate? (mechanics, ML, hybrid)
4. **Data requirements**: What's needed to build and deploy?
5. **Validation status**: How proven are they?
6. **Limitations**: What's not working?

**Example narrative** (not a list):
> Clinical digital twins for cardiac arrhythmia have achieved the most mature status, with inHEART's patient-specific ventricular tachycardia (VT) ablation guidance receiving FDA 510(k) clearance in March 2024. Johns Hopkins has deployed a similar approach in an active prospective trial, demonstrating reduced procedure time and complication rates compared to conventional mapping (Author et al., PMID:12345678). These systems integrate patient-specific cardiac anatomy from 3D imaging with mechanistic electrophysiology models (Hodgkin-Huxley equations for ion channel dynamics) coupled with real-time intracardiac recordings. By contrast, oncology digital twins remain largely in the research domain, with SOPHiA GENETICS' treatment-response prediction tool (launched October 2024) relying primarily on data-driven approaches—training machine learning models on histopathology images and genomic sequencing from patient tumors rather than mechanistic models of tumor growth. This difference reflects a key challenge: cardiac electrophysiology has well-characterized governing equations (ion channels, conduction velocity), whereas tumor growth involves dozens of interacting processes (cell proliferation, apoptosis, immune infiltration, nutrient diffusion) with poorly understood parameter values.

### 3. Novelty Gaps & Opportunities (1000–1500 words)

**Purpose**: Identify what's missing, structured as concrete research opportunities.

**Structure**:
1. **Gap statement**: What isn't being done?
2. **Why it matters**: What clinical problem would solving this address?
3. **Current attempts**: Have researchers tried? Why didn't it work?
4. **Path forward**: What would solving this look like?

**Example**:
> **Gap 1: Multi-Scale Integration**
> 
> Current digital twins typically model a single biological process at a single scale. Cardiac twins focus on electrophysiology; oncology twins predict treatment response from genomics or imaging. What's absent is integration across scales—linking molecular pathways (signaling cascades, gene expression) to cellular behavior (proliferation, apoptosis) to tissue-level outcomes (tumor growth, immune infiltration). 
> 
> This matters clinically because drug response depends on all three scales. A precision medicine digital twin would predict how a drug's molecular target (e.g., PDL1 inhibitor) affects individual patient's T-cell infiltration, then tumor shrinkage. Currently, this requires three separate models (or guesswork between them).
> 
> Early attempts at multi-scale modeling exist in computational systems biology (e.g., agent-based models of tumor microenvironments), but they remain research tools. They haven't scaled to patient-specific, real-time clinical use because: (1) Computational cost is prohibitive (millions of agents × millions of time steps), (2) Calibrating parameters at all scales requires data we don't have for most patients, (3) Regulatory pathway is unclear (FDA has no precedent for multi-scale clinical twins).
> 
> Path forward: Hybrid mechanistic-ML approaches could help. Physics-informed neural networks can embed multi-scale mechanisms while learning patient-specific parameters from available clinical data. A prospective study comparing multi-scale vs. single-scale predictions on patient cohorts would test the hypothesis that integration improves clinical accuracy.

### 4. Clinical Translation Barriers (500–1000 words)

**Purpose**: Explain why deployment is hard, even when models are accurate.

**Structure**:
- Computational barriers (real-time speed)
- Data barriers (what's needed for personalization)
- Regulatory barriers (FDA framework)
- Clinical workflow barriers (integration with EHRs, clinical decision-making)
- Validation barriers (prospective trials are expensive)

### 5. Recommendations for Your Proposal (500–1000 words)

**Purpose**: Tie findings back to your research question.

**Structure**:
- **Where your work fits**: Which gap does your proposal address?
- **Why it's novel**: How does your approach differ from what exists?
- **Why it matters**: What clinical problem does it solve?
- **Validation strategy**: How will you prove it works?
- **Regulatory/deployment path**: How will it reach patients?

---

## Writing Tips

### ✓ Do This

- **Use topic sentences**: "Cardiac digital twins have achieved clinical deployment; oncology twins remain research-stage."
- **Cite as you write**: "Smith et al. (PMID:12345678) demonstrated that..."
- **Explain acronyms**: "Physics-informed neural networks (PINNs) embed differential equations..."
- **Connect findings**: "Unlike mechanistic models [Ref], data-driven approaches [Ref] require large cohorts, which limits their use in rare diseases..."
- **Acknowledge contradictions**: "Studies disagree on whether [X]. Author A argues [reason], while Author B found [different result]. Likely explanation: [synthesis]"

### ✗ Avoid This

- Long bullet-point lists (synthesize into prose)
- One-sentence summaries of each paper (integrate findings thematically)
- Unexplained jargon
- Claims without citations
- Overstating evidence ("This proves..." when the evidence only suggests)
- Ignoring limitations (say what wasn't covered and why)

### Structure Long Sections with Headers

If a section exceeds 1500 words, break it into subsections:

```
## Current State of Digital Twins in Cardiac Disease

### Mechanistic Electrophysiology Models
[500 words]

### Data-Driven Imaging & Genomics Approaches  
[500 words]

### Hybrid & Emerging Approaches
[400 words]
```

---

## Evidence Table Support

For each major claim in the narrative, you should have a corresponding row in the evidence table:

**Narrative claim**: "Only 2–5 patient-specific digital twins have FDA clearance."

**Evidence table row**:
| Claim | Supporting Studies | PMIDs | Grade | Notes |
|-------|---|---|---|---|
| Only 2–5 patient-specific digital twins have FDA clearance | inHEART (2024), Johns Hopkins VT trial | 12345678, 87654321 | Strong | FDA 510(k) documented |

---

## Checklist Before Finalizing

- [ ] No orphaned questions (all "what is" converted to findings)
- [ ] Every claim has a citation
- [ ] All PMIDs verified in PubMed
- [ ] Narrative flows logically (not just concatenated paper summaries)
- [ ] Jargon explained on first use
- [ ] Contradictions acknowledged and explained
- [ ] Limitations of the review itself stated (scope, date range, databases searched)
- [ ] Recommendations tied back to proposal or research question
- [ ] Reading level appropriate for your audience (scientists familiar with domain? clinicians? general readers?)
