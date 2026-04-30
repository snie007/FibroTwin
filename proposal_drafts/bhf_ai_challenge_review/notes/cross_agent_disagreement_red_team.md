# Cross-agent disagreement and red-team

This note treats the proposal adversarially. Each section pits two agent perspectives against each other, then records the *strongest* counter-argument and how the proposal should respond. Citation keys correspond to entries in `refs/references.bib`.

The aim is to surface the disagreements that BHF reviewers will surface anyway, and to record them transparently rather than pretending they do not exist.

---

## Disagreement 1 - Are AI-ECG screening tools clinically useful or just diagnostically performant?

**Pro side (Engineering, Implementation).** EAGLE (`yao2021eagle`) is a positive pragmatic cluster RCT. Multiple multicentre external validations report AUC 0.85-0.96 for low EF (`attia2021external`, `lee2026model`, `lee2025ecg`, `lee2022electrocardiogram`, `knig2024electrocardiogram`). Clinical adoption is occurring (`lin2024real`, `lee2026ecg`, `goto2024effect`).

**Sceptical side (Methodologist, Reviewer).** LOOP showed that AF detection tripled but stroke did not fall (`svendsen2021loop`). VITAL-AF (`lubitz2022vitalaf`) was overall negative. A 1-year AI-ECG AF risk model in multicentre external validation reached only 31% sensitivity at 92% specificity (`pfeifer2026ecg`). Heart-failure AI-ECG meta-analysis pooled AUC 0.76 with high heterogeneity (`zhangelectroca2025electrocardiogram`).

**Strongest counter the panel will raise.** "What will *change* for the patient because of this AI-ECG model that would not change without it?"

**Programme response.** Frame each AI-ECG deployment as a *decision change* (e.g. earlier echocardiography referral, earlier HF therapy, earlier amyloid pathway), not a statistic. Pre-register the decision-change endpoint, not just the AUC.

---

## Disagreement 2 - Should LLMs appear in the BHF programme at all?

**Pro side (Engineering, Implementation).** LLM-drafted consent is more complete than surgeon free text (`miller2023llmconsent`), patient-perceived empathy is high (`ayers2023comparing`), diagnostic reasoning on complex cases is non-trivial (`eriksen2023diagnose`), and pragmatic LLM trials in cardiology workflow exist (`nctllmscreeni2024manual`, `nctmitralvide2025video`, `nctcabgai2026cabg`).

**Sceptical side (Methodologist, PPI).** GPT-4 cannot reliably cite sources for ACLS-style content (`fritsch2024knows`), LLMs are not yet equipped to fully assist anaesthesia/ICU decisions (`lyubchenkochat2025applications`), spine-surgery LLM decision support is weak for procedure choice (`bouhassiraevalu2025evaluating`), and patients are unwilling to accept autonomous AI decisions (`mawpatientaihf2025patient`).

**Strongest counter the panel will raise.** "If LLMs make it into your programme, what is your plan for patient harm caused by an LLM hallucination?"

**Programme response.** LLMs only as *supervised communication and workflow tools*; explicit non-claim that LLMs make autonomous medical decisions; explicit incident-reporting and rollback plan; explicit reliance on human-in-the-loop verification.

---

## Disagreement 3 - Is "individualised treatment-effect" estimation actually deployable?

**Pro side (Methodologist, Engineering).** Methodologically there is now a serious literature on causal-ML and dynamic treatment regimes (`curth2024causalml`, `komorowski2018reinforcement`). CABANA's comorbidity-by-treatment heterogeneity (`steinbergcaba2025association`) is exactly the kind of structure individualized models exploit.

**Sceptical side (Implementation, Reviewer).** Individualised treatment-effect models have rarely been *prospectively* deployed in cardiology, and reinforcement-learning recommendation systems have limited evidence outside ICU (`komorowski2018reinforcement`). Patients (`mawpatientaihf2025patient`) and clinicians (`bawdencardiaca2025patients`) tend to accept AI as decision support, not as treatment selector.

**Strongest counter the panel will raise.** "How will your model's recommendation be operationalised in clinic without making the clinician a rubber stamp?"

**Programme response.** Position the platform as offering *individualized, decision-supportive evidence*, not autonomous prescribing; commit to evaluation through pragmatic, embedded trials rather than algorithmic deployment alone.

---

## Disagreement 4 - Cardiomyopathy family screening - is "trajectory-based surveillance" achievable in 5 years?

**Pro side (Engineering, Methodologist).** Existing cohorts already provide the substrate: 1 365-relative DCM screening cohort with 14.1% findings (`owensdcmrelati2023screening`); 1 230-relative HCM cohort over 6 762 person-years (`michelshcmfami2024family`); HCM AI risk models with external validation (`liuhcmmlmace2024machine`); MAARS multimodal HCM arrhythmic-death model (`ahnmaarshcm2025multimodal`); HCM AI-ECG (`ko2020electrocardiogram`, `lewontin2025ecg`); HCM scar quantification (`siontishcmscar2023interpretable`, `fahmyhcmscarsc2022radiomics`).

**Sceptical side (Implementation, Reviewer).** Family screening pathways differ across NHS regions and are sensitive to genetics-service capacity. Trajectory-based surveillance changes the *frequency* of imaging, not just the *interpretation* of imaging - that requires service-redesign work that is more political than algorithmic.

**Strongest counter the panel will raise.** "Who in the NHS owns the decision to lengthen or shorten a surveillance interval, and how will your model interact with them?"

**Programme response.** Co-design with inherited cardiac conditions services (e.g. specialist nurse leads) from day 1; commit to implementation work-package on surveillance-interval governance, not only modelling.

---

## Disagreement 5 - Is the foundation-model strand evidence-justified?

**Pro side (Engineering).** Foundation models for medicine are now real (`moor2023foundation`, `singhal2023encode`); image-text echo foundation models exist (`christensen2024echoclip`); ECG foundation models support rare-disease transfer (`huelectrocard2025deep`).

**Sceptical side (Methodologist, Reviewer, PPI).** None of these have demonstrated improved patient outcomes in cardiology yet. Pre-prints dominate.

**Strongest counter the panel will raise.** "Why include foundation models if they have no patient-outcome evidence?"

**Programme response.** Include foundation-model work as a *methods strand* with infrastructure deliverables (rare-disease transfer, multimodal phenotyping), not as a clinical-outcome promise.

---

## Disagreement 6 - Equity and bias

**Pro side (PPI, Methodologist).** Equity audits are now expected by NICE / MHRA / FDA. Subgroup performance reporting is standard in TRIPOD-AI / DECIDE-AI (`collins2021tripodai`, `vasey2022decideai`). The Obermeyer paper (`obermeyer2019dissecting`) is canonical evidence that deployed risk algorithms can encode racial bias via cost as a proxy for need. Cardiology AI has its own ethnicity-related performance variation (`lewontin2025ecg`).

**Sceptical side (Engineering, Implementation).** Equity audits are sometimes used as a substitute for genuine remedial work; many deployed models have not been retrained when bias was identified.

**Strongest counter the panel will raise.** "If you find inequity, what will you actually do about it?"

**Programme response.** Pre-commit, in writing, to a remedial path: model retraining, re-deployment criteria, pause/stop conditions, and PPI sign-off for deployment changes.

---

## Disagreement 7 - Cost-effectiveness in NHS context

**Pro side (Implementation, Reviewer).** NICE evaluates digital tools through ESF; the AI/digital regulations service exists; existing AI-ECG cost-effectiveness analyses are emerging (`ehj2024aiecgcostefface`).

**Sceptical side (Methodologist, PPI).** Cost-effectiveness models depend on assumptions about downstream care that often do not hold; many AI-ECG screening pathways generate downstream investigation cascades that have not been costed.

**Strongest counter the panel will raise.** "What is the downstream investigation burden, and is it acceptable to NHS commissioners?"

**Programme response.** Build downstream-care utilization (echo, CMR, specialist referral) directly into the cost-effectiveness work-package, not as an afterthought.

---

## Cumulative red-team summary

The single most consistent theme across these disagreements is *clinical utility, not algorithmic performance*. Every BHF reviewer is likely to test the proposal against the same question: "What changes for the patient because this programme exists, and how will you measure that change in NHS data?"

The strongest defensive posture is to:

1. State the decision-change endpoints explicitly for each exemplar.
2. Pre-register external-validation cohorts and pre-specify subgroup analyses.
3. Promise lifecycle governance and equity remediation, not just audits.
4. Confine LLMs to supervised communication and workflow.
5. Position causal-ML and foundation models as methodological strands, not outcome promises.
6. Make PPI substantive and visible at programme leadership.
7. Bake regulatory and HTA work into the first tranche, not the last.
