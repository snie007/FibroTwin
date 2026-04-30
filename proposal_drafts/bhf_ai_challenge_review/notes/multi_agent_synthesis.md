# Multi-agent synthesis

This note synthesises the harvested literature through five explicit *agent perspectives*. Each agent is run as a structured re-reading of `data/master_citations.json` against a different prior, and the synthesis at the end records both convergence and disagreement. Citation keys correspond to entries in `refs/references.bib`.

The five agents:

1. **Clinical methodologist** - cares about study design, validation, calibration, and risk-of-bias.
2. **Implementation/policy expert** - cares about NHS, NICE/MHRA/HTA pathways, deployment, and governance.
3. **AI engineering lead** - cares about model architecture, data, reproducibility, and lifecycle.
4. **Patient/PPI lead** - cares about acceptability, trust, equity, and lived-experience burden.
5. **Grant reviewer (BHF panel proxy)** - cares about strategic fit, ambition, partnerships, and value for money.

The agents are run independently, then reconciled.

---

## Agent 1 - Clinical methodologist

**Read of the field.** The cardiovascular AI literature has matured into a few well-validated areas (AI-ECG low-EF screening, AI-ECG sinus-rhythm AF prediction, multicentre AI-CMR segmentation and HCM/amyloid differentiation) but remains methodologically uneven everywhere else. The systematic-review evidence is unambiguous: only 34% of clinically relevant AI-ECG models had external validation and only 11% shared implementation resources (`avulaelectroca2023clinical`); pooled AI-ECG heart-failure-prediction performance was AUC ≈ 0.76 with high heterogeneity (`zhangelectroca2025electrocardiogram`); 14-study AF systematic review showed marked between-study variability (`tsiartas2025ecg`); the EHR-AF score is one of the few prediction tools with multi-cohort external validation (`khurshid2022electronic`).

**What I want the proposal to commit to.**
- Pre-registered external-validation cohorts in NHS-representative populations, using the original model weights, not just retrained variants.
- Pre-specified subgroup analyses by age, sex, ethnicity, comorbidity, and care setting.
- TRIPOD+AI / SPIRIT-AI / CONSORT-AI / PROBAST(+AI) / DECIDE-AI compliance up front (`collins2021tripodai`, `cruzrivera2020spiritai`, `liu2020consortai`, `wolff2019probast`, `vasey2022decideai`).
- Calibration assessment, not just discrimination - decision curves and net benefit, not just AUC.
- Pre-specified analysis of *clinical utility* (not just diagnostic performance), in the spirit of EAGLE (`yao2021eagle`).

**Where I am sceptical.** Anything claimed to "transform" cardiology with single-cohort AUCs above 0.95 should be treated as needing replication before it is built into a clinical policy.

---

## Agent 2 - Implementation/policy expert

**Read of the field.** UK regulatory and HTA infrastructure for AI in healthcare is now mature enough that proposals which treat regulation as an afterthought are at a real disadvantage. NICE has explicit Evidence Standards Framework and an AI/digital regulations service; MHRA's SaMD/AIaMD roadmap (`mhra2024samdpositions`) defines lifecycle expectations; international reporting standards are set; FDA maintains a living list of cleared AI/ML medical devices that includes many cardiology examples (`fda2024aimllist`). WHO's six principles for AI in health (`who2021aiguidance`) are widely referenced.

**What I want the proposal to commit to.**
- Explicit work-package alignment with NICE ESF and the NICE AI/digital regulations service pathway.
- A specific commitment to MHRA-aligned lifecycle governance: post-market monitoring, drift detection, equity audits.
- A clear decision around what is and is not a "medical device" under the SaMD/AIaMD framework.
- Genuine NHS deployment partners with named trusts and named integration points (e.g. AI-ECG inside an NHS PACS or ECG cart workflow).
- Realism about cost-effectiveness: at least one pre-planned health-economic modelling study, e.g. for AI-ECG screening pathways (cf. `ehj2024aiecgcostefface`).

**Where I am sceptical.** Many published AI-in-cardiology proposals over-index on technical novelty and under-index on whom in the NHS will actually run, audit, and decommission these models.

---

## Agent 3 - AI engineering lead

**Read of the field.** The dominant architectural patterns in cardiovascular AI are now (a) deep convolutional / temporal models for ECG (`hannun2019cardiologist`, `ribeiro2020automatic`, `attiaecg2019enabled`, `attia2019ecg`, `ko2020electrocardiogram`), (b) U-Net-style segmentation networks for CMR (`bai2018automated`, `meyerprecision2022precision`, `hannlandmark2021landmark`), (c) multimodal fusion models for prognosis (`ahnmaarshcm2025multimodal`, `liuhcmmlmace2024machine`, `kidoctcmrmlcad2025data`, `kidoeatstressc2024quantification`), (d) transformer / foundation models (`moor2023foundation`, `huelectrocard2025deep`), and (e) LLMs and image-text models for workflow (`singhal2023encode`, `christensen2024echoclip`).

**What I want the proposal to commit to.**
- A modular architecture (phenotyping / decision / interface) so each layer can be re-trained, replaced, or audited.
- Reproducible training pipelines with public benchmarks (PTB-XL `wagner2020publicly`, MIMIC `johnson2016mimic`, PhysioNet `goldberger2000physiobank`, UK Biobank `petersen2016ukbiobank`) and clear evaluation harnesses (`strodthoff2021ptbxl`).
- Uncertainty estimation as default, not optional (`lee2022electrocardiogram`, `chenuncertainty2023automatic`, `fahmy2020t1uncertainty`).
- Explainability that is *evaluated*, not just produced (`arendselectroc2026signal`, `jang2025ecg`).
- Foundation-model strategy for transfer to rare disease and low-data subgroups (`huelectrocard2025deep`).

**Where I am sceptical.** Engineering teams overestimate how reusable an AUC-strong model is once it crosses a hospital boundary. The "external validation" literature exists for a reason.

---

## Agent 4 - Patient / PPI lead

**Read of the field.** The patient evidence is small but consistent. In an HF outpatient survey, only 18.2% were comfortable with AI acting independently, and 97.3% trusted their cardiologist over AI in disagreement (`mawpatientaihf2025patient`). A qualitative study in two English hospitals (`bawdencardiaca2025patients`) found that workflow fit, verification, and data security dominate acceptance. Both studies broadly converge: patients support AI as decision support, not as autonomous decision maker.

**What I want the proposal to commit to.**
- PPI co-investigator at programme leadership level, not just oversight committee.
- Explicit lay-summary deliverables for every AI tool, including model intent and safety claims, in plain language.
- Equity audits with explicit subgroup performance reporting and a remedial plan if performance is unequal (`obermeyer2019dissecting`).
- Realistic articulation of what patients gain, not just system efficiency.

**Where I am sceptical.** Many proposals invoke "patient and public involvement" rhetorically. The strongest version of this proposal will give PPI veto-class authority over what is and is not deployed.

---

## Agent 5 - Grant reviewer (BHF panel proxy)

**Read of the field.** The BHF Grand Challenge is up to GBP 10 million over 5 years (`bhf2026grandchallenge`) and explicitly seeks programmes that reach NHS scale, mature partnerships, and step-change impact. The clearest weakness in many AI-cardiology funding submissions is over-promising on autonomy and under-delivering on translation; the second clearest is reading as a stack of three good projects rather than one programme.

**What I want the proposal to commit to.**
- A single generalisable decision-support platform with three exemplar decisions (intervention, surveillance, follow-up) - not three independent workstreams.
- A demonstrable translational pathway from model to NHS deployment within the 5-year envelope.
- Named NHS, regulatory (NICE/MHRA), and industry partners.
- A credible health-economic story.
- An honest position on what the programme will *not* do (e.g. autonomous LLM-based clinical decisions).

**Where I am sceptical.** Funding panels will discount proposals that promise everything; they will reward proposals that promise specific, defensible, NHS-relevant outcomes.

---

## Synthesis - convergences

All five agents converge on the following:

- The strongest framing is **one decision-support platform**, with three exemplar decisions, not three projects.
- AI-ECG should be the **scalable phenotyping layer**, not the headline story.
- AI-CMR should be the **deep-phenotyping layer** for the chosen exemplars.
- LLMs belong as **supervised communication and workflow tools**, with explicit non-claims.
- External validation, regulatory alignment, equity, and PPI are **first-tranche** deliverables.
- Pragmatic NHS-embedded evaluation matters more than benchmark AUCs.

## Synthesis - residual disagreements (recorded honestly)

| Topic | Agent disagreement |
|---|---|
| LLM workflow scope | Engineering wants more LLM ambition; Methodologist and PPI want narrower, supervised use only. **Resolution**: keep LLM scope narrow in the outline; reserve broader LLM workstreams for the full application. |
| Foundation models | Engineering wants foundation-model centrality; Methodologist and Reviewer worry about evidence base. **Resolution**: include foundation-model phenotyping as a methods strand; do not promise clinical-outcome transformation from it. |
| AI-ECG vs AI-CMR centrality | Implementation prefers AI-ECG (NHS scale); Methodologist and Engineering prefer AI-CMR (deep phenotype). **Resolution**: present them as complementary layers in the same platform. |
| RL / dynamic treatment regimes | Engineering and Methodologist disagree on readiness. **Resolution**: include as a methodological aspiration tied to one exemplar, not as a programme-wide claim. |
| Cost-effectiveness | Reviewer and Implementation want it; PPI and Methodologist want it framed as utility evidence first. **Resolution**: include both, sequenced - clinical utility first, formal HTA second. |

These residual disagreements should be retained in the proposal's risk register.
