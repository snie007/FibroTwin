# AI-in-the-clinic trials review

This note summarises the trial- and deployment-grade evidence for AI in cardiology clinical pathways, drawing on `data/intermediate/llm_cv_ai_clinic_candidates.json` and the wider master corpus. Citation keys correspond to entries in `refs/references.bib`. Tabular form is in `data/tables/ai_clinic_trials_table.{csv,md,tex}`.

The aim is to separate (a) *completed RCTs and pragmatic trials*, (b) *prospective implementation studies*, (c) *ongoing trials and registry studies*, and (d) *workflow / LLM evaluations*, so that the BHF proposal can cite a defensible base of *clinical* (not just *algorithmic*) evidence.

---

## 1. Completed randomized and pragmatic trials

| Use case | Reference | Headline result |
|---|---|---|
| AF ablation versus drugs | `packercabana2019effect` | Composite endpoint 8.0% vs 9.2% (HR 0.86); ablation reduced CV hospitalisation/death (HR 0.83) and AF recurrence (HR 0.52). |
| AF ablation comorbidity heterogeneity | `steinbergcaba2025association` | Treatment effect concentrated in high-comorbidity patients (HR 0.62 vs 1.16; interaction p = 0.038). |
| AI-ECG cluster RCT for low EF (EAGLE) | `yao2021eagle` | Across 22 641 visits, AI-ECG arm had higher new low-EF diagnosis (2.1% vs 1.6%; OR 1.32). |
| AF screening with implantable loop recorder (LOOP) | `svendsen2021loop` | AF detection tripled but no stroke reduction at 5 years. |
| Smartphone AI-ECG screening (VITAL-AF) | `lubitz2022vitalaf` | No overall increase in new AF diagnoses, but increased detection in older subgroups. |
| Smartphone AI-ECG cluster RCT (Hong Kong) | `yan2024smartphoneafrct` | Reduction in cardiovascular events in older adults. |
| AliveCor + remote review (REHEARSE-AF) | `halcox2017rehearseaf` | Higher AF detection vs routine care in 1 001 elderly UK participants. |
| Apple Heart Study | `perez2019scale` | 0.52% irregular-pulse notification rate; PPV 0.84 on subsequent ECG patch (n = 419 297). |
| Smartwatch deep neural net (Tison) | `tison2018passive` | Sensitivity 98%, specificity 90% versus 12-lead ECG (cardioversion cohort). |
| AI-ECG dyskalemia alert pragmatic RCT | `linelectrocar2026enabled` | Pragmatic open-label physician-randomised RCT (n = 14 989) of real-time AI-ECG alert. |
| Pragmatic AI-ECG inpatient cluster RCT (Lin 2024) | `lin2024pragmaticaiecg` | Mortality reduction in patients flagged high-risk versus usual care. |

Quality flag: most positive AF screening trials still leave open whether new AF diagnoses translate into reduced strokes; LOOP is the cleanest negative. EAGLE is the cleanest positive cardiology AI-ECG cluster RCT to date.

---

## 2. Prospective implementation / real-world evaluations

- **AI-ECG ED integration alternating-day study** (`choi2026ecg`) - real-time AI-ECG ECG interpretation in ED workflow with diagnostic and process-metric outcomes (n = 1 524).
- **Hospital-wide ambidirectional AI-ECG cohort** (`lin2024real`) - changes in ECG read times and downstream investigations after deployment.
- **AI-ECG cardiac amyloidosis prospective deployment** (`goto2024effect`) - increased diagnosis rates with acceptable workflow burden.
- **Confidence-aware AI-ECG external validation** (`lee2022electrocardiogram`) - exclusion of low-confidence cases improved external AUC from 0.94 to 0.97.
- **External validation of AI-ECG biomarkers across US healthcare system** (`lee2026ecg`) - generalisation of Korean ECG Buddy to US data.
- **DL echo coaching for novices** (`narang2022utility`) - nurses acquired diagnostic-quality echo views with DL guidance.
- **DL echo guidance for experts** (`schneider2022real`) - improved standardisation of echo acquisition.

---

## 3. Ongoing trials and registry studies relevant to the BHF programme

| Title | Identifier | Status |
|---|---|---|
| External validation of AI-ECG for LV dysfunction | `nctaiecglvefnct2025external` (NCT07038018) | NOT_YET_RECRUITING |
| AF risk estimation with single-lead handheld ECG | `nctafscreennc2025atrial` (NCT07468123) | ENROLLING_BY_INVITATION |
| Computational imaging for VT ablation | `nctaivtnctcom2024computational` (NCT06964152) | ENROLLING_BY_INVITATION |
| International AI-CMR cardiomyopathy diagnosis study | `nctaidmrnctin2023international` (NCT05793840) | UNKNOWN |
| Willem AI-ECG platform multicentre cohort | `nctwillemnctc2023ai` (NCT05890716) | RECRUITING |
| DETECT-AS aortic-stenosis personalised monitoring | `nctdetectasnct2026deep` (NCT06749132) | NOT_YET_RECRUITING |
| TARTAN-HF targeted screening for HF in diabetes | `ncttartanhfnct2022targeted` (NCT05705869) | ACTIVE_NOT_RECRUITING |
| LLM-assisted clinical-trial screening | `nctllmscreeni2024manual` (NCT06588452) | RECRUITING |
| Mitral-valve AI-generated peri-operative video education | `nctmitralvide2025video` (NCT07036926) | RECRUITING |
| CABG AI-supported discharge education | `nctcabgai2026cabg` (NCT07503678) | NOT_YET_RECRUITING |
| ML in AF phenotyping cohort | `nctmlafnctaf2020machine` (NCT05371405) | RECRUITING |
| ML-driven AF identification RCT | `nctafalgorith2019randomised` (NCT04045639) | COMPLETED |

These cover the four pillars BHF reviewers will look for: external validation, ongoing implementation trials, LLM workflow trials, and procedural-AI trials. Several already have NHS-relevant analogues (e.g. TARTAN-HF, REHEARSE-AF infrastructure).

---

## 4. LLM and workflow-deployment evidence

- **Consent generation**: `miller2023llmconsent` - LLM-drafted consent more complete and readable than surgeon free text.
- **Patient social-media questions**: `ayers2023comparing` - LLM responses preferred for empathy.
- **Diagnostic reasoning**: `eriksen2023diagnose` - GPT-4 ranked correct diagnosis in top 3 in 64% of NEJM Clinicopathologic Conference cases.
- **Cardiology systematic review**: `cortes2026llmcardiologyreview` - 33 studies; promising in education/ECG, inconsistent in emergency advice.
- **Cardiology-specific framing**: `khera2023chatgptcv`.
- **Anaesthesia and ICU**: `lyubchenkochat2025applications` - LLMs not yet equipped to fully assist physicians.
- **Spine surgery decision support**: `bouhassiraevalu2025evaluating` - usable for triage, weak for procedure selection.
- **Source-citation reliability**: `fritsch2024knows` - GPT-4 cannot reliably cite sources for ACLS-style content.
- **Patient-facing readability of IR documents**: `winklercanlarg2025better`, `bagheridelivery2024large`.
- **Anaesthesia preoperative education**: `aksuartificia2026artificial`.
- **Perioperative drug interactions**: `caputochatgpt2026chatgpt`.
- **Trainee education in OMFS**: `parkerlargela2026large`.

The bottom-line synthesis is: LLMs *belong* in the BHF programme only as supervised communication and workflow assistants; the evidence supports patient education, summarisation, consent drafts, and recruitment screening; the evidence does not support autonomous procedural or emergency decisions.

---

## 5. Implications for the BHF outline

1. The proposal should cite at least one positive pragmatic AI cluster RCT (EAGLE) and one negative AI-screening trial (LOOP) to demonstrate methodological honesty.
2. The proposal should cite at least one ongoing UK or NHS-relevant trial to anchor implementation feasibility.
3. The proposal should explicitly frame LLM workflows as supervised, with patient and clinician acceptability evidence (`mawpatientaihf2025patient`, `bawdencardiaca2025patients`) cited as motivation.
4. Procedural-AI exemplars (e.g. `nctaivtnctcom2024computational`, `nctaiimagingg2024computational`) provide concrete patterns the proposal can adapt for AF ablation, ICD decisions, and structural intervention selection.
