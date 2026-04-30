# Background literature review for the BHF AI challenge concept

Note: direct access to the Overleaf project was blocked during collection, so this review is based on the preliminary abstract plus publicly accessible call documents, guidelines, and publications.

## Core proposition being tested

The abstract argues that cardiovascular care still relies too heavily on static risk models, while real clinical decisions need:

1. individual treatment effect estimation, not just baseline risk prediction
2. longitudinal latent-state modelling, not cross-sectional snapshots
3. multimodal fusion across EHR, imaging, physiology, and wearables
4. clinically safe de-escalation rules, especially where high negative predictive value matters

The three proposed clinical anchors are well chosen because each exposes a different failure mode of current practice:

- *AF ablation*: average treatment effects obscure who really benefits
- *Cardiomyopathy family screening*: categorical surveillance schedules are blunt and likely over-monitor some relatives while under-detecting others
- *Post-MI care*: risk and treatment needs evolve after discharge, but follow-up systems are still coarse and episodic

---

## 1) Clinical perspective

### A. Atrial fibrillation ablation: there is real treatment-effect heterogeneity to model

*CABANA* is the cleanest starting point for the "risk is not benefit" argument.

- In 2,204 patients across 126 centres in 10 countries, the primary endpoint occurred in *8.0%* of the ablation group versus *9.2%* of the drug-therapy group, HR *0.86* (95% CI 0.65 to 1.15), so the average intention-to-treat effect on the primary composite was not significant. But ablation still reduced death or cardiovascular hospitalization, *51.7% vs 58.1%*, HR *0.83* (95% CI 0.74 to 0.93), and AF recurrence, *49.9% vs 69.5%*, HR *0.52* (95% CI 0.45 to 0.60). PMID: *30874766*.
- The most proposal-relevant message is that average trial effects are mixed because the cohort is mixed.

Newer CABANA subgroup analyses strengthen that point.

- In a post hoc comorbidity analysis, the adjusted HR for ablation versus drug therapy on the primary outcome was *0.62* (95% CI 0.42 to 0.93) in patients with *high comorbidity burden* versus *1.16* (95% CI 0.76 to 1.77) in low-burden patients, interaction *P=0.038*. PMID: *41213867*.
- In a frailty analysis, event reduction was not clearly different by frailty, but quality-of-life gains were. Frail patients receiving ablation had MAFSI frequency improvement of *-1.58* (95% CI -2.11 to -1.06) and severity improvement of *-1.26* (95% CI -1.69 to -0.84), both *P<0.001*. PMID: *41652456*.

This is exactly the kind of setting where individualized treatment effect estimation could outperform conventional guideline heuristics.

### B. AF ablation: multimodal phenotyping already shows clinically meaningful gradient effects

The *DECAAF* study shows why multimodal phenotyping matters.

- Among patients undergoing first AF ablation, day-475 recurrent arrhythmia climbed from *15.3%* in stage-1 fibrosis to *69.4%* in stage-4 fibrosis.
- Every *1%* increase in left atrial fibrosis was associated with recurrence HR *1.06* (95% CI 1.03 to 1.08).
- Adding fibrosis to a conventional recurrence model increased the C statistic from *0.65 to 0.69*. PMID: *24496537*.

Clinically, that says the proposal should not frame imaging, physiology, and EHR as optional add-ons. They are part of the phenotype that determines likely benefit and recurrence.

### C. Cardiomyopathy family screening: current surveillance is necessary, but probably too blunt

For dilated cardiomyopathy relatives, the screening yield is high enough to justify active surveillance.

- In *1,365* first-degree relatives, *14.1%* had new DCM-related findings: *2.1%* DCM, *3.6%* LV systolic dysfunction, *8.4%* LV enlargement. PMID: *37225358*.
- The key quote is that screening identified findings in *"1 in 7"* reportedly unaffected first-degree relatives, regardless of race and ethnicity.

For hypertrophic cardiomyopathy relatives, the story is more nuanced.

- In *1,230* relatives from *531* families, the baseline combined clinical and genetic yield was *26%*.
- Over *6,762 person-years* and a mean *7 years* of follow-up, only *43* additional relatives developed HCM, an incremental yield of *4%*.
- In gene-elusive families, only *2* relatives, *0.4%*, with baseline wall thickness *<10 mm* developed HCM on follow-up. PMID: *39365224*.

That low-yield tail is where trajectory modelling could have immediate clinical value: identifying who can be safely monitored less often.

### D. Existing cardiomyopathy policy is categorical, not dynamic

The current HCM surveillance framework is structured but coarse.

From the ACC/AHA HCM guidance summary:

- genotype-positive or early-onset pediatric families: ECG/echo every *1 to 2 years*
- other pediatric relatives: every *2 to 3 years*
- adults: every *3 to 5 years*
- variant pathogenicity should be revisited every *2 to 3 years*

Useful quote: *"Screening first-degree family members ... can begin at any age and can be influenced by specifics of the patient/family history and family preference."* Source: `hcm-guidelines-made-simple-2020.pdf`.

That is a strong opening for a proposal that moves from age-band rules to trajectory-informed intensity.

### E. Post-MI care: longitudinal optimization is plausible and clinically relevant

The post-MI workstream is slightly less mature in the collected literature than AF and cardiomyopathy, but the rationale is still strong.

- NICE explicitly frames acute coronary syndromes as needing both early and longer-term rehabilitation management. Source: NICE NG185.
- In a 2026 STEMI cohort of *1,863* patients, 1-year mortality was *13.6%* and a parsimonious 5-feature ML model achieved an AUC of *0.821*. PMID: *41688111*.
- A 2025 systematic review included *30* studies using ECG, imaging, and EHR data for acute myocardial ischemia diagnosis, risk stratification, and decision support. PMID: *41523481*.

So the clinical case is not that AI for post-MI care is absent. It is that current tools are mostly point predictions, while the proposal wants dynamic treatment and follow-up optimization over time.

### Clinical take-home

The strongest clinical pitch is:

- AF ablation gives a compelling treatment-effect heterogeneity use case.
- Cardiomyopathy family screening gives a compelling surveillance-intensity use case.
- Post-MI care gives a compelling dynamic follow-up and secondary-prevention use case.

---

## 2) Engineering perspective

### A. The proposal addresses a real technical gap, not just a clinical slogan

A foundational cardiovascular AI review argued that traditional statistical methods may struggle with complex biomedical and healthcare data. PMID: *29352006*.

The engineering novelty should be described as the combination of three hard problems:

1. *heterogeneous treatment effect estimation* in high-dimensional observational data
2. *latent temporal-state inference* from irregular longitudinal data
3. *multimodal fusion* across asynchronous sources with missingness and unequal reliability

If the application treats these as separate side-projects, it will feel fragmented. If it presents them as one decision-engine stack, it will feel programmatic.

### B. The proposal should emphasize clinically constrained objectives, not generic model performance

Good engineering framing for this call:

- optimize for *negative predictive value* where safe non-intervention matters
- calibrate risk over time, not only discrimination at baseline
- show subgroup performance by sex, ancestry, deprivation, age, and disease severity
- design models to generate *actionable outputs*: offer ablation, intensify surveillance, de-escalate follow-up, escalate rehab

DECAAF is useful here because it shows incremental predictive gain from a richer phenotype, but only modestly if handled as a conventional model, C-statistic *0.65 to 0.69*. PMID: *24496537*. That supports more ambitious fusion rather than single-modality add-ons.

### C. Parsimony will help adoption

The STEMI mortality paper is useful because the best model used only *5* variables and still achieved AUC *0.821*. PMID: *41688111*.

That is a useful design warning: the programme should not default to the most complex multimodal transformer everywhere. Reviewers may respond better if the proposal says:

- use the richest model where it materially improves decisions
- distill or simplify outputs where parsimonious models are enough
- build deployment pathways that are realistic for NHS data availability

### D. Engineering risks that must be named explicitly

Recent cardiology AI reviews repeatedly emphasize:

- generalizability limits
- workflow integration failures
- algorithmic bias
- poor explainability
- regulatory burden

PMIDs: *38901544*, *40151850*.

If the proposal sounds too confident about cross-site transfer or silent background deployment, that will hurt it.

### Engineering take-home

The engineering section should read less like "we will apply AI" and more like:

- we will build decision-grade longitudinal multimodal models
- we will benchmark them against simple policy baselines and parsimonious models
- we will optimize for safety, calibration, and transportability
- we will pre-plan monitoring, drift checks, and subgroup auditing

---

## 3) Grant reviewer perspective

### A. What this idea has going for it

This concept maps unusually well onto the BHF call language.

The call wants:

- *"AI-powered transformation in cardiovascular health: From discovery to clinical practice"*
- a *"step-change in impact or ambition"*
- large integrated programmes, not small standalone projects
- meaningful lived-experience involvement
- robust management and governance
- explicit path to translation and impact

The proposal also naturally spans:

- cardiovascular disease burden
- methodological novelty
- multimodal data
- clinical translation
- NHS relevance

### B. What reviewers may worry about

1. *Too broad.* AF, cardiomyopathy, and post-MI could look like three mini-programmes unless tied together by one methodological core.
2. *Too much method, not enough implementation.* BHF wants research, but also a real path to patient benefit.
3. *Causal claims in observational data.* Reviewers will push hard on confounding, target-trial logic, and validation.
4. *Data access realism.* Do the teams already control the required imaging, EHR, genetic, and wearable streams?
5. *Weak health-economics or NHS adoption plan.* NICE and HTA readiness matter.

### C. What will strengthen the application

The application should probably be framed as 3 linked workstreams plus 2 cross-cutting platforms:

- WS1: individualized treatment effect estimation in AF ablation
- WS2: trajectory-based surveillance for inherited cardiomyopathy relatives
- WS3: dynamic post-MI follow-up and treatment optimization
- Platform A: multimodal temporal learning and causal inference methods
- Platform B: implementation science, regulation, health economics, and patient involvement

That structure matches the scale BHF expects.

### D. Numbers and phrases worth echoing back to BHF

From the call material:

- award size: *up to £10 million over 5 years*
- *smaller standalone projects are unlikely to be competitive*
- there will be a *formal review after the first year*
- PIs from AI or data science backgrounds are welcome
- meaningful lived experience involvement is expected

### Grant reviewer take-home

The application will land best if it is presented as a *generalizable decision-making platform* demonstrated in three high-value cardiovascular settings, not three disconnected disease projects.

---

## 4) Patient perspective

### A. Patients do not want fully autonomous AI in cardiology

This is one of the clearest patient-side findings in the collected evidence.

In a heart-failure survey of *110* patients:

- *38.1%* were happy for their doctor to use AI help in treatment decisions
- only *18.2%* were comfortable with AI acting *without* physician input
- only *21.8%* were comfortable with AI remotely adjusting treatment with fewer in-person visits
- *80.9%* preferred cardiologist diagnoses
- *84.6%* preferred cardiologist treatment plans
- *97.3%* would trust their cardiologist over AI in cases of disagreement

PMID: *41346424*.

That is a major design implication. The proposal should not talk like the system will replace expert judgement.

### B. Patients and clinicians in England describe AI as an adjunct, not a replacement

A qualitative study in two English hospitals found that patients, clinicians, and developers were broadly positive about AI, but wanted:

- clinician verification
- human empathy
- transparency about AI use
- data security
- better workflow fit

Sample: *9* patients, *16* clinicians, *5* developers. PMID: *40534891*.

### C. Why the cardiomyopathy workstream is patient-important

Family screening has both emotional and logistical burden. Current policies are deliberately cautious, but blunt scheduling can mean:

- repeated low-yield testing
- uncertainty that drags on for years
- unnecessary visits for very-low-risk relatives
- delayed escalation for the higher-risk group who do need closer follow-up

The HCM family-screening paper is powerful here because it suggests that some relatives are at genuinely very low follow-up yield, only *0.4%* conversion in one subgroup over long follow-up. PMID: *39365224*.

### D. Why the AF workstream is patient-important

If frail patients gain more quality-of-life improvement from ablation than non-frail patients, then a patient-centred AI programme should not be fixated only on mortality or hospitalization. PMID: *41652456*.

### Patient take-home

The user-facing value proposition should be:

- fewer unnecessary procedures and visits
- earlier escalation when trajectories worsen
- more transparent, individualized recommendations
- clinician-supervised AI that supports, rather than replaces, trusted care relationships

---

## 5) Policy expert perspective

### A. The NHS policy environment is receptive, but not permissive by default

The most important policy signal is that UK institutions now expect AI programmes to think beyond model accuracy.

- NICE ESF: digital tools need evidence matched to function and risk, and the framework was updated in *2022* to include AI and adaptive algorithms.
- NICE AI/digital regulations service: explicitly maps the regulatory and HTA pathway.
- MHRA roadmap: *11 work packages* across two workstreams for SaMD and AIaMD.
- NHS AI code of conduct: *10 principles* for data-driven technology used by the NHS.
- FDA AI SaMD policy: reinforces lifecycle management, transparency, and predetermined change control planning.

### B. Health inequalities and fairness are not optional extras

Several NICE pages explicitly restate commissioner duties to reduce health inequalities. The MHRA roadmap also explicitly mentions inclusive innovation and the need for AIaMD to perform across diverse populations.

That means the proposal should pre-specify:

- representation audits
- fairness analyses
- subgroup calibration/performance reporting
- governance for data drift and reclassification
- what happens when performance is worse in an under-served group

### C. Why policy experts may like the cardiomyopathy workstream

Because it fits a policy problem they already understand: surveillance intensity is being managed with categorical rules, but guidelines themselves already admit that timing can be influenced by family history and preference.

### D. Why policy experts may worry about the AF and post-MI workstreams

Because treatment optimization algorithms can drift into opaque decision support without clear accountability, approval pathway, or reimbursement logic.

So the proposal should say early that it will produce:

- research outputs
- clinically interpretable decision tools
- evidence packages aligned to NICE ESF and MHRA expectations
- monitored, human-supervised deployment models

### Policy take-home

This project can be made policy-attractive if it is framed as *responsible clinical AI infrastructure*, not just a prediction project.

---

## Cross-cutting synthesis

### The most persuasive narrative for the proposal

Current cardiovascular care often asks the wrong question.

- Standard models ask: *who is high risk?*
- Clinicians need to ask: *who benefits from what, when, and with what follow-up intensity?*

The collected evidence supports exactly that reframing:

- AF: average ablation effects conceal meaningful heterogeneity
- Cardiomyopathy: repeated family surveillance has non-trivial yield overall, but likely over-surveils low-yield subgroups
- Post-MI: there is real opportunity for longitudinal risk updating and targeted follow-up
- Patients: want clinician-supervised AI, not autonomy theatre
- Policy: wants evidence, fairness, governance, and implementation realism

## Best evidence anchors for the final narrative

If the final document has to stay short, the highest-yield anchors are probably:

1. *CABANA* for average effect vs individualized benefit, PMID *30874766*
2. CABANA comorbidity analysis for explicit treatment-effect heterogeneity, PMID *41213867*
3. *DECAAF* for multimodal phenotyping and recurrence gradient, PMID *24496537*
4. DCM family screening yield, PMID *37225358*
5. HCM low-yield follow-up subgroup, PMID *39365224*
6. HCM guideline surveillance intervals, PMID *38718139* plus ACC guideline summary PDF
7. HF patient attitudes toward AI, PMID *41346424*
8. NICE ESF and MHRA roadmap for implementation legitimacy
9. BHF Grand Challenge guidance for proposal tailoring

## Recommended one-line thesis

*This programme will move cardiovascular AI from static event prediction toward individualized decisions about intervention, surveillance, and follow-up intensity, using multimodal longitudinal data and an explicitly deployable NHS-facing evidence framework.*
