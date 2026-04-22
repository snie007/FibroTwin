# PMID verification log, ventricular arrhythmias R01 aims page

This file provides the two extra reviewer-style checks requested by the user:

- **Verifier A: reference existence check** — does the PMID resolve to a real, online PubMed record?
- **Verifier B: claim mapping check** — does the title/abstract actually support the sentence it is being used for?

## Verifier A, online existence check

All PMIDs below were resolved through PubMed E-utilities and returned valid article metadata.

- **PMID 29097296** — 2017 AHA/ACC/HRS Guideline for Management of Patients With Ventricular Arrhythmias and the Prevention of Sudden Cardiac Death.
- **PMID 31075787** — 2019 HRS/EHRA/APHRS/LAHRS expert consensus statement on catheter ablation of ventricular arrhythmias.
- **PMID 37283271** — 2023 HRS/APHRS/LAHRS guideline on cardiac physiologic pacing for the avoidance and mitigation of heart failure.
- **PMID 31993492** — Brugada syndrome: A comprehensive review of pathophysiological mechanisms and risk stratification strategies.
- **PMID 33421051** — Brugada syndrome and reduced right ventricular outflow tract conduction reserve: a final common pathway?
- **PMID 36542434** — Delayed depolarization and histologic abnormalities underlie the Brugada syndrome.
- **PMID 34777827** — The Use of Electrocardiographic Imaging in Localising the Origin of Arrhythmias During Catheter Ablation of Ventricular Tachycardia.
- **PMID 15649241** — Challenges facing validation of noninvasive electrical imaging of the heart.
- **PMID 33303478** — Translational applications of computational modelling for patients with cardiac arrhythmias.
- **PMID 32448065** — Considering discrepancy when calibrating a mechanistic electrophysiology model.
- **PMID 25368538** — Effects of fibrosis morphology on reentrant ventricular tachycardia inducibility and simulation fidelity in patient-derived models.
- **PMID 35715087** — Conduction System Pacing for Cardiac Resynchronization Therapy.
- **PMID 37767743** — Effectiveness of conduction system pacing for cardiac resynchronization therapy: A systematic review and network meta-analysis.
- **PMID 38323181** — The role of computational methods in cardiovascular medicine: a narrative review.

## Verifier B, claim mapping check

### Strong claim matches

- **PMID 31075787** strongly supports the burden and clinical importance of ventricular arrhythmias because the abstract explicitly states that ventricular arrhythmias are an important cause of morbidity and mortality.
- **PMID 37283271** strongly supports the pacing / CRT / conduction-system pacing portions because the abstract explicitly defines cardiac physiologic pacing as including CRT and CSP and says it may mitigate or prevent heart failure.
- **PMID 34777827** strongly supports the ECGi limitation statements because the abstract explicitly says ECGi solves the inverse problem, that human accuracy has varied, and that it is likely not accurate enough to guide more discrete radiofrequency ablation.
- **PMID 15649241** strongly supports the statement that the inverse problem is highly ill-posed because the abstract says exactly that.
- **PMID 33421051** strongly supports the Brugada conduction-substrate framing because the abstract discusses RVOT conduction delay and proposes reduced RVOT conduction reserve as a final common pathway.
- **PMID 36542434** strongly supports statements about delayed depolarization and structural myocardial abnormalities in Brugada syndrome.
- **PMID 33303478** strongly supports the translational rationale for patient-specific computational modeling in arrhythmia care because it explicitly discusses improving standard-of-care therapy, personalising treatment plans, and resynchronisation therapy planning.
- **PMID 32448065** strongly supports the need for calibration and uncertainty awareness in mechanistic electrophysiology models.
- **PMID 25368538** strongly supports the linkage between fibrosis morphology, structural substrate, and VT inducibility in patient-derived ventricular models.
- **PMID 35715087** and **PMID 37767743** strongly support the claim that conventional CRT response is variable and that conduction-system pacing is being evaluated as an alternative or improvement.

### Moderate claim matches, usable but should be phrased carefully

- **PMID 29097296** is highly authoritative for ventricular arrhythmia / sudden death framing, but the abstract text is not available in PubMed. It should be cited for broad guideline-level context rather than a precise sentence that depends on abstract wording.
- **PMID 31993492** is a strong general Brugada review and supports statements about arrhythmic risk and disputed mechanisms, but more specific claims about RVOT substrate and conduction reserve are better anchored by PMID 33421051 and PMID 36542434.
- **PMID 38323181** supports broad translational value of computational cardiovascular models, but the arrhythmia-specific translational claims are more directly supported by PMID 33303478.

## Reviewer warning list

These are points to avoid over-claiming unless stronger or more specific citations are added later in the full application:

- Do not claim that ECGi can never identify substrate; the safer wording is that it does not robustly identify underlying substrate and has important inverse-problem limitations.
- Do not claim that forward-calibrated models are already proven to improve outcomes; the safer wording is that they may improve localisation, classification, and prediction and will be prospectively tested.
- Do not overstate mechanistic consensus in Brugada syndrome; use wording that acknowledges ongoing debate while highlighting evidence for conduction/substrate abnormalities.

## Recommended use in later passes

- Use the PMIDs above as explicit anchors in each reviewer pass.
- When a sentence changes materially, re-check whether the mapped PMID still supports the revised wording.
- For the final R01, expand beyond this aims-page map into a larger evidence table for Significance, Innovation, and Approach.
