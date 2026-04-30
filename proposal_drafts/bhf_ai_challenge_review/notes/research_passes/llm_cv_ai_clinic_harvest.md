# LLM, cardiovascular AI, and “AI clinic” literature harvest

Date: 2026-04-30

## Purpose

This pass harvests a broad evidence base around LLMs and AI in cardiovascular care, with emphasis on three translational layers:

1. disease detection and longitudinal phenotyping,
2. treatment or surveillance decision support,
3. workflow-facing "AI clinic" functions such as education, consent, discharge, triage, and trial screening.

A structured machine-readable candidate set is in `data/intermediate/llm_cv_ai_clinic_candidates.json`.

## Bottom line

The strongest cardiovascular AI evidence is still in narrow but clinically meaningful tasks such as AI-ECG screening, imaging-supported phenotyping, family-screening risk enrichment, and post-MI prognostic modelling. The translational frontier is moving from retrospective accuracy papers toward prospective validation, screening pilots, and workflow-embedded studies.

For LLMs, the evidence base is much earlier. Most published work supports supervised use in communication and workflow tasks, not autonomous cardiology decision-making. The most realistic "AI clinic" near-term model is therefore a layered service:

- **core clinical AI** for phenotype detection, risk enrichment, and prioritization,
- **prospective evaluation** in screening, procedural guidance, and monitoring pathways,
- **LLM interface tools** for patient explanation, discharge education, MDT summarization, and recruitment operations, always with human verification.

## Evidence map by theme

### 1) High-maturity cardiovascular AI use cases

**AI-ECG and inexpensive latent phenotyping** are the clearest mature line of evidence.

- AI-enabled ECG for reduced LVEF showed external-test AUC 0.93 and predicted future ventricular dysfunction, suggesting routine ECG can recover latent structural disease (`Attia2019AIECGLVEF`).
- AF-from-sinus-rhythm work showed AUC 0.87 from a single ECG and 0.90 with serial ECGs, which supports low-friction enrichment for AF case finding (`Attia2019AIECGAF`).
- HCM and amyloidosis AI-ECG studies suggest cheap physiology can detect structural or infiltrative phenotypes well before routine diagnosis in some patients (`Ko2020AIECGHCM`, `Grogan2021AIECGAmyloid`).
- Confidence-aware AI-ECG work is especially relevant to safe deployment because it explicitly separates high- and low-confidence outputs (`Cho2022AIECGConfidence`).

**Decision support around intervention and surveillance** is plausible, but evidence is still piecemeal.

- CABANA remains the anchor randomized trial for AF ablation, while newer heterogeneity analysis suggests benefit is not uniform and may concentrate in higher-comorbidity patients (`Packer2019CABANA`, `Steinberg2025CABANAComorbidity`).
- DECAAF shows why imaging matters, because fibrosis load strongly stratifies post-ablation recurrence (`Marrouche2014DECAAF`).
- Family-screening cohorts in DCM and HCM show that some relatives have meaningful near-term yield while others have very low incremental yield over repeated follow-up, which is exactly where dynamic surveillance models could matter (`Owens2023DCMRelatives`, `Michels2024HCMFamilyScreen`).
- Post-MI AI evidence is now broad enough to justify a pathway-focused workstream, but most models still predict events rather than optimize follow-up intensity or treatment changes (`Ahmad2025PostMIMeta`).

### 2) Prospective and ongoing clinical deployment signals

The registry/trial landscape is important because it shows where the field is actually trying to operationalize AI.

**AI-ECG deployment and validation**
- `NCT07038018AIECGLVEF`: multicentre external validation of AI-ECG for reduced LVEF, explicitly focused on transportability.
- `NCT07468123AFScreen`: prospective pilot using prior AI risk to enrich single-lead handheld AF screening.
- `NCT05890716WILLEM`: multicentre study of cloud AI ECG interpretation in high-risk cardiac patients.
- `NCT06749132DETECTAS`: deep-learning-enhanced personalized monitoring in aortic stenosis.

**Imaging and procedure-guidance AI**
- `NCT06964152AIVT`: prospective use of computational ECG and cardiac imaging analysis to guide VT ablation, with recurrent VT and mortality as endpoints.
- `NCT05793840AIDMRI`: international MRI-based cardiomyopathy diagnosis and complication-prediction validation study.
- `NCT05371405MLAF`: prospective AF phenotyping study seeking better ablation outcome prediction.

**Pathway and clinic-style screening workflows**
- `NCT05705869TARTANHF`: randomized targeted assessment in high-risk diabetes to detect undiagnosed heart failure, relevant to AI-enabled case finding embedded in service lines.
- `NCT04045639AFAlgorithm`: completed ML-based AF identification trial using risk prediction plus diagnostic testing.

These studies matter because they are closer to an "AI clinic" than benchmark papers are. They test whether algorithmic enrichment can change who gets screened, prioritized, or procedurally guided.

### 3) LLM evidence in cardiology and adjacent peri-procedural care

The LLM literature is broadening, but still mostly supports **adjacent workflow roles**.

**Published support functions**
- Better structured informed-consent documentation than routine clinician-generated text has been reported in common procedures (`Miller2023LLMConsent`).
- Cardiology-focused systematic review work finds promise in education and ECG interpretation, but weak evidence for high-stakes autonomous guidance and too much reliance on vignette or in silico testing (`Cortes2026LLMCardiologyReview`).

**Ongoing workflow-facing trials relevant to cardiovascular services**
- `NCT06588452LLMScreening`: LLM-assisted heart-failure trial screening versus manual review.
- `NCT07036926MitralVideoAI`: AI-generated peri-operative education for mitral valve surgery.
- `NCT07503678CABGAI`: AI-supported individualized discharge education after CABG.

This is the clearest current "AI clinic" pattern: the LLM layer is not the diagnostic engine. It is the operational, educational, and documentation interface wrapped around conventional care and narrower predictive models.

### 4) Implementation constraints that recur across the literature

- **Prospective evidence is still sparse.** Many headline cardiovascular AI papers remain retrospective.
- **Transportability is uneven.** External validation is improving, but subgroup performance remains a major concern.
- **Clinician oversight is non-negotiable.** Patient and qualitative implementation studies consistently frame AI as adjunctive, not autonomous (`Maw2025PatientAIHF`, `Bawden2025CardiacAIQual`).
- **LLMs are workflow tools first.** The strongest credible claims are around readability, discharge support, documentation, and screening operations, not independent treatment decisions.

## Suggested framing for proposal development

A credible BHF-facing "AI clinic" concept would be:

- a **cardiovascular intelligence service** built around multimodal risk enrichment and longitudinal prioritization,
- tested in **specific pathway entry points** such as family screening, AF enrichment, post-MI follow-up, HF case finding, or procedure planning,
- with **LLMs positioned as supervised interface tools** for communication, MDT summarization, trial matching, and patient education.

That framing avoids overclaiming while still sounding ambitious and translational.

## Candidate trial and registry shortlist

| Citation key | Focus | Status | Why it matters |
|---|---|---:|---|
| `NCT07038018AIECGLVEF` | AI-ECG external validation for reduced LVEF | Not yet recruiting | Direct transportability study for a leading AI-ECG use case |
| `NCT07468123AFScreen` | AI-enriched handheld AF screening | Enrolling by invitation | Tests whether prior AI risk can improve real screening yield |
| `NCT06964152AIVT` | AI-guided VT ablation | Enrolling by invitation | One of the clearest prospective procedural-guidance studies |
| `NCT05793840AIDMRI` | AI-MRI cardiomyopathy diagnosis/prognosis | Unknown | Multisite validation of multimodal structural phenotyping |
| `NCT05890716WILLEM` | AI ECG platform in high-risk cardiac patients | Recruiting | Real workflow deployment of cloud ECG AI |
| `NCT06749132DETECTAS` | Deep-learning monitoring in aortic stenosis | Not yet recruiting | Precision surveillance rather than one-off diagnosis |
| `NCT05705869TARTANHF` | Targeted screening for undiagnosed HF | Active, not recruiting | Good exemplar of service-line screening deployment |
| `NCT05371405MLAF` | Machine learning in AF phenotyping | Recruiting | Links ML phenotyping to ablation outcome prediction |
| `NCT04045639AFAlgorithm` | ML AF identification trial | Completed | Early completed example of algorithm-guided case finding |
| `NCT06588452LLMScreening` | LLM-assisted HF trial screening | Recruiting | Strong "AI clinic operations" use case |
| `NCT07036926MitralVideoAI` | AI-generated mitral surgery education | Recruiting | Prospective cardiovascular peri-operative education study |
| `NCT07503678CABGAI` | AI-supported CABG discharge education | Not yet recruiting | Tests individualized post-op communication and recovery support |

## Gaps to keep in mind

1. Very little evidence yet supports autonomous LLM decision-making in cardiology.
2. Even strong AI-ECG evidence does not by itself prove pathway benefit, cost-effectiveness, or NHS workflow fit.
3. The most novel opportunity is probably not another static predictor, but a service model that links:
   - low-friction signals,
   - multimodal adjudication,
   - pathway prioritization,
   - patient-facing explanation and follow-up.

## Files produced in this pass

- `notes/research_passes/llm_cv_ai_clinic_harvest.md`
- `data/intermediate/llm_cv_ai_clinic_candidates.json`
