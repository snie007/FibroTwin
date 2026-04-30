# Extensive review: LLMs and AI in cardiovascular care

This note synthesises the harvested literature in `data/intermediate/` and `data/master_citations.json` (n = 233 unique citations) into a long-form review aligned with the BHF AI Cardiovascular Grand Challenge framing. Citation keys correspond to entries in `refs/references.bib`.

The aim is not encyclopaedic coverage but a defensible map of where evidence is mature, where it is weak, and where the BHF programme can credibly add value over the next five years.

---

## 1. Where the field actually is

### 1.1 Mature, deployable, but narrow
Three areas now have multi-cohort external validation, regulatory clearance, and at least one pragmatic trial.

- **AI-ECG for low ejection fraction.** The Mayo derivation cohort (`attiaecg2019enabled`, AUC 0.93 in 52 870 patients) was followed by the EAGLE pragmatic cluster RCT in 22 641 primary-care visits across 45 sites, where AI-ECG screening increased new low-EF diagnoses (`yao2021eagle`). Independent external validation has reproduced AUC ≈ 0.88-0.96 in non-Mayo cohorts (`knig2024electrocardiogram`, `attia2021external`, `lee2026model`, `lee2025ecg`). Confidence-aware deployment improved external AUC from 0.94 to 0.97 after low-confidence exclusion (`lee2022electrocardiogram`).
- **AI-ECG for atrial fibrillation prediction during sinus rhythm.** The original AUC-0.87 derivation in 180 922 patients (`attia2019ecg`) is now supported by multicentre external validation with realistic operating points (sensitivity 31% / specificity 92% in `pfeifer2026ecg`), a systematic review of 14 studies and 33 models (`tsiartas2025ecg`), and integration with left-atrial size data (`hirota2026prediction`). Cluster-randomised population AF screening trials provide a stable comparator base (`svendsen2021loop`, `lubitz2022vitalaf`, `yan2024smartphoneafrct`, `halcox2017rehearseaf`) and consumer-grade wearables now have FDA clearance and large-cohort evidence (`perez2019scale`, `apple2018apple`, `tison2018passive`, `bumgarner2018smartwatch`).
- **AI-CMR segmentation, fibrosis quantification, and amyloid/HCM differentiation.** Multicentre, multi-vendor validation is mainstream. Examples: precision LV segmentation across 3 309 scans with scan-rescan testing (`meyerprecision2022precision`); UK-Biobank-scale automated phenotyping (`bai2018automated`, `petersen2016ukbiobank`); landmark detection across cine/LGE/T1 mapping with 96-100% success on 531 hold-out cases (`hannlandmark2021landmark`); diagnosis across 11 cardiovascular diseases with AUC 0.99 internally and externally (`zhangaienabled2024screening`); HCM-versus-amyloid differentiation across 56 institutions (`michelmulticen2025multicenter`); HCM scar quantification with r = 0.92 to manual labels (`siontishcmscar2023interpretable`); MAARS multimodal HCM-arrhythmic-death model with external AUC 0.81 (`ahnmaarshcm2025multimodal`).

These three areas can be characterised as ready for *prospective embedding* and *health-economic* evaluation rather than further pure model development.

### 1.2 Promising but inconsistent
Several use cases have published AUCs in the 0.85-0.95 range but recurring problems with calibration, subgroup transportability, and clinical-utility evidence:

- AI-ECG for cardiac amyloidosis (`groganamyloido2021enhanced`, `gonzlezlpez2026amyloidosis`, `jainamyloidosi2026detecting`, `goto2024effect`).
- AI-ECG for hypertrophic cardiomyopathy (`ko2020electrocardiogram`, `lewontin2025ecg`, `baburguler2026electrocardiogram`).
- AI-ECG for aortic stenosis (`kim2025electrocardiogram`, `wu2025aiecgaorticstenosis`).
- AI-ECG for pulmonary hypertension (`liu2022electrocardiogram`, `herreraleao2026ecg`).
- AI-ECG for coronary heart disease and ischaemia (`zhang2025electrocardiogram`, `lim2026ecg`, `park2025ecg`).
- LGE/T1-based myocarditis assessment (`pleinaimyocard2024imaging`, `kim2023t2mapping_dl_validation`, `aly2022myocarditis_cnnkcl`).

In each case, performance varies substantially across cohorts (e.g. AI-ECG HCM differs by ethnicity in `lewontin2025ecg`; multi-institution AI-ECG AF prediction varies by site in `suzuki2026enhanced`). They are credible workstreams *only if* deployment design and validation across NHS-representative data are first-class deliverables.

### 1.3 Early or hypothesis-generating
Foundation models, multimodal cardiac AI, and LLM-supported decision support are still mostly in development:

- **Foundation models** for medical AI (`moor2023foundation`) and cardiology-specific image-text models such as EchoCLIP (`christensen2024echoclip`) provide infrastructure but no convincing clinical-outcome evidence yet.
- **LLM/cardiology**. The 2026 systematic review (`cortes2026llmcardiologyreview`) found 33 studies dominated by in-silico evaluation: education and ECG interpretation are promising; emergency advice is inconsistent. ChatGPT-class models can generate ACLS-style answers but cannot reliably cite sources (`fritsch2024knows`). Even pragmatic adoption studies (`ayers2023comparing`, `eriksen2023diagnose`, `singhal2023encode`, `khera2023chatgpt`) frame LLMs as workflow assistants, not autonomous decision-makers.
- **Wearable-AI deep biomarkers** (`khurshid2024detect`, `lee2025ecg`, `lin2026electrocardiogram`) suggest single-lead ECG can reach hospital-grade signal but field deployment evidence is shallow.
- **Multi-modal genotype-free phenotyping** (`natcvres2024genotypefreecmr`, `raisiestabragh2023genetics`, `raisiestabragh2024noninvasive`) hints at population-scale phenotyping but is downstream of biobank infrastructure.

### 1.4 Where there is *not yet* good evidence
- Individualised treatment-effect estimation that *actually changes* who gets ablation, ICD, valve intervention, or surveillance intensity.
- Time-updated longitudinal risk that recalibrates as new ECGs / scans / labs arrive.
- Patient-level prospective evidence that LLM-supported workflow reduces clinician burden without harming safety.
- Demonstrated cost-effectiveness for AI-ECG, AI-CMR, or LLM workflow in NHS-representative populations.

These gaps are exactly what BHF reviewers will look for the programme to fill.

---

## 2. Synthesis by clinical decision

### 2.1 Intervention decisions (e.g. AF ablation)
The clearest case for *individualised treatment-effect* AI is AF ablation. CABANA showed mixed average benefit (`packercabana2019effect`) but explicit comorbidity-by-treatment heterogeneity (HR 0.62 in high-comorbidity vs 1.16 in low-comorbidity, interaction p = 0.038) (`steinbergcaba2025association`). DECAAF showed atrial fibrosis from CMR stratified recurrence from 15.3% to 69.4% across stages (`marrouchedecaa2014association`). AI-ECG / AI-CMR phenotyping (`bai2018automated`, `attiaecg2019enabled`) is now scalable enough to feed individualised treatment-effect models in routine NHS data, and ongoing trials (`nctmlafnctaf2020machine`, `nctaipowereda2023ai`, `nctaiimagingg2024computational`, `nctafalgorith2019randomised`) provide a real comparator base.

### 2.2 Surveillance intensity (e.g. inherited cardiomyopathy family screening)
The DCM relatives study (`owensdcmrelati2023screening`, 14.1% findings in 1 365 first-degree relatives) and HCM family-screening cohort (`michelshcmfami2024family`, 26% baseline yield but only 0.4% conversion in low-risk gene-elusive subgroup) imply that current 1-2-3-5-year surveillance bands are coarse. AI-ECG (`ko2020electrocardiogram`, `lewontin2025ecg`), AI-CMR HCM scar prediction (`siontishcmscar2023interpretable`, `fahmyhcmscarsc2022radiomics`), and HCM event-prediction models with external validation (`liuhcmmlmace2024machine`, `ahnmaarshcm2025multimodal`) collectively provide the building blocks for a trajectory-based, risk-adapted surveillance policy.

### 2.3 Follow-up intensity after acute events (e.g. post-MI, post-STEMI)
Static prognostic models are well-developed: meta-analysis pooled C-index 0.77 across 28 studies and 59 392 patients (`ahmadpostmimet2025accuracy`), and DeepSTEMI achieved external AUC 0.894 across three centres (`zhangdeepstemi2025novel`). The next step is *time-updated* care-policy modelling, where reinforcement learning (`komorowski2018reinforcement`) and causal-ML methods (`curth2024causalml`) could in principle support pragmatic dynamic-treatment trials.

### 2.4 Communication, consent, and workflow
LLMs belong here, narrowly. Strong evidence: LLM-drafted consent more complete and readable than surgeon free text (`miller2023llmconsent`); LLM responses to social-media questions often preferred for empathy (`ayers2023comparing`); pragmatic workflow trials such as LLM-assisted screening (`nctllmscreeni2024manual`) and AI-generated peri-operative video education (`nctmitralvide2025video`, `nctcabgai2026cabg`). Weak or warning evidence: ChatGPT cannot reliably cite sources (`fritsch2024knows`); LLMs not yet ready to assist anaesthesia/ICU decisions (`lyubchenkochat2025applications`); spine-surgery decision support better at triage than procedure choice (`bouhassiraevalu2025evaluating`).

### 2.5 Implementation, governance, and patient trust
Patients in HF clinic accept AI as decision support (97.3% would trust their cardiologist over AI in disagreement; only 18.2% comfortable with AI acting alone) (`mawpatientaihf2025patient`). Qualitative work in two English hospitals (`bawdencardiaca2025patients`) shows workflow fit, verification, and data security dominate acceptance. UK regulatory infrastructure - NICE ESF, NICE AI/digital regulations service, MHRA SaMD/AIaMD roadmap (`mhra2024samdpositions`), TRIPOD-AI / SPIRIT-AI / CONSORT-AI / DECIDE-AI / PROBAST (`collins2021tripodai`, `liu2020consortai`, `cruzrivera2020spiritai`, `vasey2022decideai`, `wolff2019probast`) - is mature enough that the proposal should treat regulatory and HTA work packages as *first-tranche* deliverables, not afterthoughts.

---

## 3. Maturity vs weakness map (explicit flagging)

| Area | Evidence maturity | Key weaknesses |
|---|---|---|
| AI-ECG low EF screening | High; pragmatic RCT (EAGLE) | Limited NHS-representative external validation; no UK cost-effectiveness |
| AI-ECG AF prediction | High; multicentre external validation | Sensitivity often <50% at usable specificity; subgroup transportability |
| AI-CMR segmentation | High | Free-text reporting / workflow integration evidence still limited |
| AI-CMR cardiomyopathy diagnosis | Medium-high | Few prospective utility studies |
| AI-ECG amyloid / HCM / AS / PH detection | Medium | Calibration drift; limited deployment trials |
| Multi-modal HCM event prediction | Medium | No prospective trial of decision change |
| LLM patient education / consent / workflow | Medium for completeness, low for safety | Hallucination, citation failure, supervised review essential |
| LLM emergency / procedural decisions | Low | Inconsistent across models and topics; not safe as autonomous |
| Reinforcement-learning dynamic care | Conceptual / very early | Reward design, off-policy evaluation, clinician adoption |
| Foundation models for cardiology | Early | No clinical-outcome evidence yet |
| Causal-ML treatment-effect estimation | Methodologically mature, clinically scarce | Few prospective deployments outside oncology |
| Health economics of cardiovascular AI | Very limited | Single illustrative analyses; little NHS-specific |
| Cost-effective and equitable deployment | Very limited | Bias audits often retrospective only (`obermeyer2019dissecting`) |

---

## 4. Implications for the BHF programme

1. The programme should **not** be framed as another cardiovascular AI prediction-score effort. It should be framed as moving from *static risk* to *individualized decisions* about intervention, surveillance, and follow-up intensity.
2. AI-ECG should be the **enabling phenotyping and screening layer**, not the headline product.
3. AI-CMR should be the **deep phenotyping layer** for the chosen exemplar cohorts.
4. LLMs should appear only as **supervised communication and workflow tools**, with explicit safety claims and explicit non-claims.
5. Validation, regulatory, HTA, and patient/public-involvement work should be **first-tranche** deliverables, not appendices.
6. The exemplar decisions (AF ablation, inherited cardiomyopathy surveillance, post-MI follow-up) are well-supported by trials, registry studies, and family-screening cohorts. They are also the decisions where individualization most plausibly changes practice.
