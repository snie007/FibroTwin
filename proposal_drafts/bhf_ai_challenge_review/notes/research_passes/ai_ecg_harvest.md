# AI-ECG harvest for BHF review

Total candidate citations harvested: **62** (PubMed-indexed studies/reviews plus official commercial sources).

## Why this pass is high value

- Deliberately weighted toward studies likely to survive into a 50-row evidence table: seminal derivation papers, external validations, prospective or pragmatic studies, systematic reviews/meta-analyses, and deployment/commercial signals.
- Coverage spans AI-ECG methods, AF screening from sinus rhythm, LV dysfunction and heart failure, structural heart disease screening, ischemia/chest-pain use cases, implementation, explainability/open-science issues, and commercial translation.
- Metadata were pulled from Europe PMC/PubMed records where possible; commercial entries come from locally saved official product pages already in the workspace.

## Bucket counts

- **Reviews, methods, and reporting quality**: 12
- **Atrial fibrillation detection and prediction**: 11
- **LV systolic dysfunction and heart failure**: 12
- **Structural heart disease, cardiomyopathy, and ischemia**: 15
- **Implementation, deployment, and enabling methods**: 9
- **Commercial and real-world deployment signals**: 3

## Fast takeaways for the review team

- The strongest mature evidence remains in **latent disease screening from routine 12-lead ECGs**, especially low EF/LV dysfunction, occult AF, HCM, amyloidosis, pulmonary hypertension, and aortic stenosis.
- **External validation is improving but still patchy**. Several 2025 to 2026 studies address multicenter validation and pragmatic deployment, but reproducibility and subgroup robustness remain recurrent weaknesses.
- The most proposal-relevant translational framing is **AI-ECG as a scalable phenotyping or enrichment layer**, not as a stand-alone decision-maker.
- **Commercial deployment is real already** (AliveCor, Anumana, Philips/Cardiologs), which helps the implementation narrative, but academic-quality independent validation is still the safer evidentiary anchor.

## Reviews, methods, and reporting quality

1. **AI Applications in Electrocardiography for Ischemic and Structural Heart Disease: A Review of the Current State** (2026; PMID 41517565; DOI 10.3390/jcm15010316)
   - Type: review. Modality: 12-lead ECG. Condition: left ventricular systolic dysfunction / low EF.
   - Why it matters: Cardiovascular disease is the leading cause of morbidity and mortality worldwide, with ischemic and structural heart diseases being key contributors. While the 12-lead electrocardiogram (ECG) is a common low-cost diagnostic test, its interpretation is limited by human variability.
   - Status: review. Suggested key: `kim2026ai`

2. **Artificial Intelligence Applied to Electrocardiograms Recorded in Sinus Rhythm for Detection and Prediction of Atrial Fibrillation: A Scoping Review** (2026; PMID 41597485; DOI 10.3390/medicina62010199)
   - Type: scoping review. Modality: 12-lead ECG. Condition: atrial fibrillation / occult AF.
   - Why it matters: Background and Objectives: Subclinical paroxysmal atrial fibrillation (AF) is often undetected by conventional screening strategies, until complications emerge. Artificial intelligence (AI) applied to sinus rhythm electrocardiograms has emerged as a promising tool to identify individuals with occult AF and to predict the risk of future incident AF.
   - Status: evidence synthesis. Suggested key: `mrak2026electrocardiogram`

3. **Artificial Intelligence-Enabled Electrocardiography in Practice: A State-of-the-Art Review** (2026; PMID 41866890; DOI 10.4070/kcj.2025.0486)
   - Type: state-of-the-art review. Modality: 12-lead ECG. Condition: atrial fibrillation / occult AF.
   - Why it matters: Artificial intelligence-enabled electrocardiography (AI-ECG) has rapidly advanced from experimental models to clinically deployed tools. This review outlines the evolution of AI-ECG across key domains including arrhythmia detection, structural heart disease diagnosis, and digital biomarker development.
   - Status: review. Suggested key: `lee2026practice`

4. **Artificial Intelligence in Cardiac Electrophysiology: A Comprehensive Review** (2025; PMID 41295237; DOI 10.3390/jpm15110532)
   - Type: review. Modality: 12-lead ECG. Condition: atrial fibrillation / occult AF.
   - Why it matters: Background: Artificial Intelligence (AI) is a transformative innovation designed to enable machines to perform tasks typically requiring human intelligence. Among various medical fields, cardiology-and particularly electrophysiology-has seen rapid integration of AI technologies.
   - Status: review. Suggested key: `cipollone2025cardiac`

5. **Artificial Intelligence in Electrocardiography: From Automated Arrhythmia Detection to Predicting Hidden Cardiovascular Disease** (2025; PMID 41069568; DOI 10.7759/cureus.94065)
   - Type: review. Modality: 12-lead ECG. Condition: atrial fibrillation / occult AF.
   - Why it matters: Cardiovascular diseases are among the most prevalent and deadly diseases affecting humans. The most widely used diagnostic tool to interrogate cardiovascular physiology and function is an electrocardiogram (ECG).
   - Status: review. Suggested key: `elantary2025automated`

6. **Artificial intelligence capabilities in identifying atrial fibrillation using baseline sinus rhythm ECG : a systematic review** (2025; PMID 41173515; DOI 10.1136/openhrt-2025-003657)
   - Type: systematic review. Modality: 12-lead ECG. Condition: atrial fibrillation / occult AF.
   - Scale/cohort: 1459653.
   - Why it matters: 14 studies and 33 AI models were analysed. Participant data were available for 13 studies, totalling 1459653 patients, with one study providing only testing dataset data.
   - Status: evidence synthesis. Suggested key: `tsiartas2025ecg`

7. **Artificial intelligence in cardiovascular diagnostics: a systematic review and descriptive analysis of clinical applications and diagnostic performance** (2025; PMID 41315941; DOI 10.1186/s12872-025-05327-x)
   - Type: systematic review. Modality: 12-lead ECG. Condition: AI-ECG methods / evidence synthesis.
   - Why it matters: Systematic review mapped the expanding diagnostic footprint of cardiovascular AI across ECG, imaging, and multimodal applications, but emphasized heterogeneity in validation quality and limited direct comparability across studies.
   - Status: evidence synthesis. Suggested key: `niazai2025cardiovascular`

8. **Artificial intelligence in electrocardiogram-based prediction of heart failure: a systematic review and meta-analysis** (2025; PMID 41552681; DOI 10.3389/fcvm.2025.1659298)
   - Type: systematic review. Modality: 12-lead ECG. Condition: heart failure.
   - Scale/cohort: 11 cohorts; 1,728,134 participants.
   - Why it matters: Meta-analysis of ECG-based AI for heart-failure prediction found pooled performance around 0.76 with high heterogeneity, suggesting promise but limited transportability and clinical-validity evidence.
   - Status: evidence synthesis/meta-analysis. Suggested key: `zhang2025electrocardiogram`

9. **Precision Medicine for Electrocardiogram Interpretation: Clinical Relevance, Challenges, and Advances** (2025; PMID 41524056; DOI 10.31083/rcm47007)
   - Type: review. Modality: 12-lead ECG. Condition: AI-ECG methods / evidence synthesis.
   - Why it matters: Electrocardiograms (ECGs) remain a foundational pillar of cardiovascular diagnostics, providing rapid, non-invasive diagnosis and being universally accessible to all clinicians. An ECG captures the electrical signals of the heart via a standard 12-lead configuration, offering insights into arrhythmias, conduction delays, ischemic injury, structural remodeling, and systemic pathologies with cardiac implications.
   - Status: review. Suggested key: `namjouyan2025electrocardiogram`

10. **Scalable screening for structural heart disease: promises from artificial intelligence-electrocardiogram tools** (2025; PMID 40703114; DOI 10.1093/ehjdh/ztaf048)
   - Type: commentary / translational review. Modality: 12-lead ECG. Condition: AI-ECG methods / evidence synthesis.
   - Why it matters: Short translational review arguing that AI-ECG could enable scalable structural-heart-disease screening, while stressing the need for careful pathway design, confirmatory testing, and implementation evidence.
   - Status: review/commentary. Suggested key: `antoniades2025electrocardiogram`

11. **The Use of Artificial Intelligence in ECG Interpretation in the Outpatient Setting: A Scoping Review** (2025; PMID 41209885; DOI 10.7759/cureus.94113)
   - Type: scoping review. Modality: 12-lead ECG. Condition: AI-ECG methods / evidence synthesis.
   - Why it matters: Cardiovascular disease remains the leading cause of death across all demographics globally. The 12-lead ECG is a key diagnostic tool for early detection; however, its interpretation is complex and prone to error, particularly in outpatient settings.
   - Status: evidence synthesis. Suggested key: `neupane2025ecg`

12. **Clinical Applications, Methodology, and Scientific Reporting of Electrocardiogram Deep-Learning Models: A Systematic Review** (2023; PMID 38288263; DOI 10.1016/j.jacadv.2023.100686)
   - Type: systematic review. Modality: 12-lead ECG. Condition: AI-ECG methods / evidence synthesis.
   - Scale/cohort: 44 manuscripts; 53 unique models.
   - Why it matters: Systematic review found only 34% of clinically relevant ECG deep-learning models had external validation and only 11% shared code or implementation resources, underscoring major reproducibility gaps.
   - Status: evidence synthesis. Suggested key: `avula2023electrocardiogram`

## Atrial fibrillation detection and prediction

1. **12-lead electrocardiogram-based artificial intelligence model accurately predicts near-term atrial fibrillation in patients with embolic stroke of undetermined source** (2026; PMID 41908195; DOI 10.1016/j.hroo.2025.12.014)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: atrial fibrillation / occult AF.
   - Why it matters: In embolic stroke of undetermined source, a 12-lead AI model identified patients at higher near-term AF risk, supporting targeted rhythm monitoring after apparently cryptogenic stroke.
   - Status: retrospective validation in stroke-enriched cohort. Suggested key: `tomura2026electrocardiogram`

2. **A Deep Neural Network for Interpreting Wearable Electrocardiogram Data in Atrial Fibrillation: Prospective Observational Diagnostic Accuracy Study** (2026; PMID 42024548; DOI 10.2196/82475)
   - Type: prospective diagnostic accuracy study. Modality: wearable/single-lead ECG. Condition: atrial fibrillation / occult AF.
   - Scale/cohort: 116.
   - Why it matters: The sensitivity and specificity for detecting AF/AFL were 91.9% (204.9/223.0 h) and 99.6% (242.4/243.5 h), respectively. The sensitivity for detecting AF was 96.2% (191.5/199.0 h), whereas it was 55.8% (13.4/24.0 h) for detecting AFL.
   - Status: prospective/real-world evaluation. Suggested key: `rantula2026electrocardiogram`

3. **Artificial Intelligence Software for Detecting Paroxysmal Atrial Fibrillation from Sinus Rhythm Monitor ECG: Development and Clinical Trial** (2026; PMID 41455001; DOI 10.1007/s12325-025-03461-8)
   - Type: clinical trial. Modality: wearable/single-lead ECG. Condition: atrial fibrillation / occult AF.
   - Scale/cohort: 54.
   - Why it matters: Cross-validation during development yielded mean sensitivity 84.2% and specificity 66.2%; the best tuned model achieved 84.9% sensitivity and 69.9% specificity on the separate set. In the clinical trial, among 24 patients with AF documented within 7 days and 20 controls, the device showed sensitivity 91.7% (95% confidence interval (CI) 73.0-99.0) and specificity 65.0% (40.8-84.6).
   - Status: prospective/real-world evaluation. Suggested key: `tamura2026ecg`

4. **Artificial Intelligence-Enabled Electrocardiography for Preoperatively Detecting Atrial Fibrillation and Mortality Risk in Patients with Sinus Rhythm** (2026; PMID 41583521; DOI 10.7150/ijms.123598)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: atrial fibrillation / occult AF.
   - Why it matters: Background: Pre-existing atrial fibrillation (AF) and postoperative new-onset AF (NOAF) are independent perioperative risk factors associated with increased short-term mortality and adverse events. This study aimed to develop and validate an artificial intelligence (AI) model capable of detecting hidden AF, including both pre-existing AF and NOAF, from sinus rhythm electrocardiograms, to improve perioperative risks a
   - Status: development plus validation. Suggested key: `lee2026preoperatively`

5. **Artificial Intelligence-Enhanced Electrocardiography for Predicting Paroxysmal Atrial Fibrillation From Sinus Rhythm: Impact of Data Integration Across Institutions and Devices** (2026; PMID 41657013; DOI 10.1111/anec.70159)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: atrial fibrillation / occult AF.
   - Scale/cohort: 172,613.
   - Why it matters: Model F2, fine-tuned on homogeneous datasets from cardiology departments, showed consistently high performance (AUC: A1 = 0.885, A2 = 0.829, A3 = 0.845). Model F1, fine-tuned on heterogeneous datasets, demonstrated lower performance (AUC: A1 = 0.837, A2 = 0.726, A3 = 0.660).
   - Status: observational/model-development study. Suggested key: `suzuki2026enhanced`

6. **Artificial intelligence in atrial fibrillation - Timely diagnosis, risk assessment and personalized management** (2026; PMID 41611206; DOI 10.1016/j.ipej.2026.01.011)
   - Type: review. Modality: wearable/single-lead ECG. Condition: atrial fibrillation / occult AF.
   - Why it matters: Atrial fibrillation (AF) is the most common sustained cardiac arrhythmia worldwide and is associated with substantial morbidity and mortality, including stroke, systemic embolism, heart failure, and dementia. Timely diagnosis, accurate risk stratification, and personalized management are necessary to improving outcomes.
   - Status: review. Suggested key: `chatterjee2026atrial`

7. **Multicenter validation of an artificial intelligence-enabled ECG model to predict 1-year risk of atrial fibrillation or flutter** (2026; PMID 41956270; DOI 10.1016/j.hrthm.2026.03.1956)
   - Type: external validation study. Modality: 12-lead ECG. Condition: atrial fibrillation / occult AF.
   - Scale/cohort: 4,017 patients across 3 sites.
   - Why it matters: Multicenter external validation of a 1-year AF-risk model found sensitivity 31% and specificity 92% at a prespecified threshold, supporting use as a targeted enrichment tool rather than a stand-alone detector.
   - Status: multicenter external validation. Suggested key: `pfeifer2026ecg`

8. **Prediction of Atrial Fibrillation Using Artificial Intelligence-Enhanced Electrocardiography　- Does Left Atrial Size Matter?** (2026; PMID 42036324; DOI 10.1253/circj.cj-25-1151)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: atrial fibrillation / occult AF.
   - Scale/cohort: 12,595 patients without prior AF.
   - Why it matters: Among patients with high AI-ECG AF probability, incident AF rose sharply with larger left atrial diameter, reaching 11.6% per year in the largest-LA group, helping define whom to monitor more intensively.
   - Status: retrospective prognostic validation. Suggested key: `hirota2026prediction`

9. **AI-ECG for early detection of atrial fibrillation: First-year results from a stroke prevention study in Shimizu, Japan** (2025; PMID 40621219; DOI 10.1002/joa3.70132)
   - Type: retrospective cohort/model development. Modality: wearable/single-lead ECG. Condition: atrial fibrillation / occult AF.
   - Scale/cohort: 11.
   - Why it matters: AI-ECG risk determination correlated with AF detection in a Japanese healthy cohort, especially in the aged population, supporting its utility as a population-based screening tool.
   - Status: prospective/real-world evaluation. Suggested key: `masumura2025ecg`

10. **Artificial Intelligence in the Diagnosis and Management of Atrial Fibrillation** (2025; PMID 41153234; DOI 10.3390/diagnostics15202561)
   - Type: review. Modality: 12-lead ECG and digital AF tools. Condition: atrial fibrillation / occult AF.
   - Why it matters: Artificial intelligence (AI) has increasingly become a transformative tool in cardiology, particularly in diagnosing and managing atrial fibrillation (AF), the most prevalent cardiac arrhythmia. This review aims to critically assess and synthesize current AI methodologies and their clinical relevance in AF diagnosis, risk prediction, and therapeutic guidance.
   - Status: review. Suggested key: `ica2025diagnosis`

11. **An artificial intelligence-enabled ECG algorithm for the identification of patients with atrial fibrillation during sinus rhythm: a retrospective analysis of outcome prediction** (2019; PMID 31378392; DOI 10.1016/s0140-6736(19)31721-0)
   - Type: validation study. Modality: 12-lead ECG. Condition: atrial fibrillation / occult AF.
   - Scale/cohort: 180,922 patients; 649,931 sinus-rhythm ECGs.
   - Why it matters: Single-ECG AI prediction of occult AF from sinus rhythm reached AUC 0.87, improving to 0.90 with serial ECGs, supporting ECG-based enrichment for AF screening.
   - Status: retrospective derivation/validation. Suggested key: `attia2019ecg`

## LV systolic dysfunction and heart failure

1. **Artificial Intelligence-Driven Electrocardiogram Screening for Asymptomatic Left Ventricular Systolic Dysfunction in the General Population** (2026; PMID 41849876; DOI 10.1016/j.jacadv.2026.102660)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: left ventricular systolic dysfunction / low EF.
   - Scale/cohort: 1,841.
   - Why it matters: Among 60,711 ECG-TTE pairs, 32 cases (0.054%) met the criteria for LVSD. The AiTiALVSD model demonstrated excellent discrimination (AUROC 0.973; AUPRC 0.328), with a sensitivity of 90.6%, specificity of 99.4%, positive predictive value of 7.7%, and a negative predictive value of 100%.
   - Status: prospective/real-world evaluation. Suggested key: `rhee2026electrocardiogram`

2. **Artificial Intelligence-Enabled ECG Analysis to Predict Incident Heart Failure** (2026; PMID 41730522; DOI 10.1161/circheartfailure.125.013927)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: heart failure.
   - Scale/cohort: 636.
   - Why it matters: The test sets comprised MGH (13 954 individuals, 441 events, age 57±13 years, 48% women), BWH (54 396 individuals, 1809 events, age 57±13 years, 55% women), and BIDMC (25 457 individuals, 901 events, age 57±13 years, 53% women). Over 10 years, the cumulative risk of HF was 4.6% (95% CI, 4.1-5.0) in MGH, 5.0% (4.8-5.2) in BWH, and 4.4% (4.1-4.7) in BIDMC.
   - Status: observational/model-development study. Suggested key: `khurshid2026ecg`

3. **Artificial Intelligence-Enhanced Electrocardiogram Models for Detection of Left Ventricular Dysfunction: A Comparison Study** (2026; PMID 41564731; DOI 10.1016/j.jacadv.2025.102572)
   - Type: model comparison study. Modality: 12-lead ECG. Condition: left ventricular systolic dysfunction / low EF.
   - Scale/cohort: 1,203.
   - Why it matters: Comparison study of AI-enhanced ECG models for LV dysfunction found substantial performance variation across published approaches, reinforcing the importance of calibration, validation setting, and model choice before deployment.
   - Status: comparative evaluation / external validation. Suggested key: `croon2026electrocardiogram`

4. **Artificial intelligence-enhanced electrocardiography for identifying subclinical left ventricular dysfunction in hypertensive individuals: a comprehensive clinical evaluation** (2026; PMID 41852610; DOI 10.3389/fcvm.2026.1761335)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: left ventricular systolic dysfunction / low EF.
   - Scale/cohort: 134.
   - Why it matters: Subclinical LV dysfunction was identified in 134 participants (38.5%). The AI-ECG probability score differed markedly between the abnormal GLS group and the normal GLS group (0.61 ± 0.20 vs.
   - Status: retrospective derivation/validation. Suggested key: `bayraktar2026enhanced`

5. **Deep Learning Model Using Transfer Learning for Detecting Left Ventricular Systolic Dysfunction: Retrospective Algorithm Development and Validation Study** (2026; PMID 42030497; DOI 10.2196/83127)
   - Type: external validation study. Modality: 12-lead ECG. Condition: left ventricular systolic dysfunction / low EF.
   - Why it matters: The recalibrated 12-lead DeepECG LVSD model achieved an area under the receiver operating curve of 0.956 (95% CI 0.946-0.965) for internal validation and 0.940 (95% CI 0.936-0.945) for external validation of follow-up TTE-ECG pairs. The uncalibrated 12-lead DeepECG LVSD model also showed modest performance, with an area under the receiver operating curve of 0.953 (95% CI 0.941-0.965) in the internal validation and 0.
   - Status: external validation. Suggested key: `lee2026model`

6. **Deep learning algorithm for detection of acute heart failure using standard ECG waveforms** (2026; PMID 41624566; DOI 10.1093/ehjdh/ztaf132)
   - Type: external validation study. Modality: 12-lead ECG. Condition: left ventricular systolic dysfunction / low EF.
   - Scale/cohort: 603.
   - Why it matters: Aims To develop and evaluate a deep learning model for immediate and accurate diagnosis of acute heart failure(HF) using standard 12-lead electrocardiogram(ECG) waveforms collected from a large cohort of patients. Methods and results We retrospectively analysed patients aged > 18 years who underwent transthoracic echocardiogram, n -terminal pro-B type natriuretic peptide (NT-proBNP) evaluation, and ECG within one wee
   - Status: external validation. Suggested key: `lee2026ecg`

7. **AI-Enabled Smartwatch ECG: A Feasibility Study for Early Prediction and Prevention of Heart Failure Rehospitalization** (2025; PMID 40139860; DOI 10.1016/j.jacbts.2025.01.005)
   - Type: retrospective cohort/model development. Modality: smartwatch ECG. Condition: heart failure.
   - Why it matters: Feasibility study suggesting smartwatch ECG plus AI may help anticipate heart-failure rehospitalization, but the evidence is still early-stage and best viewed as hypothesis-generating.
   - Status: feasibility study. Suggested key: `lee2025ecg`

8. **An Artificial Intelligence-Enabled Electrocardiogram to Evaluate Patients With Dyspnea in the Emergency Department** (2025; PMID 41133167; DOI 10.1016/j.mayocpiqo.2025.100652)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: acute dyspnea / heart failure triage.
   - Scale/cohort: 2412.
   - Why it matters: Of the 2412 patients, 966 (40%) were found to have cardiac dyspnea, and the remaining 1446 (60%) were noncardiac. The AI-ECG-estimated diastolic function was divided into 4 groups: 922 (38.2%) were normal, 245 (10.2%) grade 1, 1192 (49.4%) grade 2, and 53 (2.2%) grade 3.
   - Status: observational/model-development study. Suggested key: `yu2025electrocardiogram`

9. **Artificial Intelligence-Enabled ECG Screening for LVSD in LBBB: Evaluating Model Development and Transfer Learning Approaches** (2025; PMID 40845745; DOI 10.1016/j.jacadv.2025.102089)
   - Type: external validation study. Modality: 12-lead ECG. Condition: left ventricular systolic dysfunction / low EF.
   - Scale/cohort: 364,845.
   - Why it matters: In external validation, the transfer learning model achieved the highest AUROC (0.903; 95% CI: 0.887-0.918), closely followed by the general model (0.899; 95% CI: 0.883-0.915); the difference was not significant. Models using automated or expert-based LBBB extraction had lower AUROCs (0.879 and 0.841, respectively).
   - Status: external validation. Suggested key: `lee2025ecg`

10. **Artificial intelligence-based identification of left ventricular systolic dysfunction from 12-lead electrocardiograms: external validation and advanced application of an existing model** (2024; PMID 38505486; DOI 10.1093/ehjdh/ztad081)
   - Type: external validation study. Modality: 12-lead ECG. Condition: left ventricular systolic dysfunction / low EF.
   - Scale/cohort: external cohort size not clearly extracted.
   - Why it matters: External validation of an existing AI-ECG LV systolic dysfunction model showed AUROC about 0.88 overall, but weaker performance in tachycardia, AF, and wide-QRS subgroups.
   - Status: external validation. Suggested key: `knig2024electrocardiogram`

11. **Artificial intelligence-enabled electrocardiogram screens low left ventricular ejection fraction with a degree of confidence** (2022; PMID 36532114; DOI 10.1177/20552076221143249)
   - Type: external validation study. Modality: 12-lead ECG. Condition: left ventricular systolic dysfunction / low EF.
   - Scale/cohort: not clearly extracted.
   - Why it matters: Confidence-aware AI-ECG for low EF improved internal AUC from 0.9549 to 0.9759 and external AUC from 0.9365 to 0.9653 after excluding low-confidence cases; high-confidence positives had markedly elevated future LV dysfunction risk.
   - Status: internal plus external validation with uncertainty stratification. Suggested key: `lee2022electrocardiogram`

12. **Screening for cardiac contractile dysfunction using an artificial intelligence-enabled electrocardiogram** (2019; PMID 30617318; DOI 10.1038/s41591-018-0240-2)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: left ventricular systolic dysfunction / low EF.
   - Scale/cohort: 44,959 training; 52,870 testing.
   - Why it matters: AI-enabled ECG screening for low ejection fraction achieved AUC 0.93, sensitivity 86.3%, and specificity 85.7%; among those without baseline dysfunction, a positive screen predicted about 4.1-fold higher future risk of ventricular dysfunction.
   - Status: retrospective derivation with temporal/holdout testing. Suggested key: `attia2019electrocardiogram`

## Structural heart disease, cardiomyopathy, and ischemia

1. **Artificial Intelligence-Enabled Electrocardiographic Detection of Severe Aortic Stenosis Leading to Transcatheter Aortic Valve Replacement** (2026; PMID 41778935; DOI 10.1016/j.jaccas.2026.107184)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: left ventricular systolic dysfunction / low EF.
   - Why it matters: Background EchoNext is an artificial intelligence (artificial intelligence)-enabled electrocardiographic (ECG) model validated to detect unrecognized structural heart disease. First-in-human/early reports summary An 84-year-old woman presented after a fall and was found to have a left femur fracture.
   - Status: observational/model-development study. Suggested key: `tat2026electrocardiographic`

2. **Deep learning model for identifying significant tricuspid regurgitation using standard 12-lead electrocardiogram** (2026; PMID 41437957; DOI 10.1016/j.ijcrp.2025.200557)
   - Type: external validation study. Modality: 12-lead ECG. Condition: atrial fibrillation / occult AF.
   - Scale/cohort: 5432.
   - Why it matters: The diagnostic performance of the DL model using ECG signals, age, and sex to predict significant TR was as follows: an accuracy of 0.762, sensitivity of 0.809, specificity of 0.756, and an area under the curve (AUC) of 0.857. After incorporating additional factors such as RR interval, QRS duration, corrected QT interval, atrial fibrillation, and hypertension into the DL model, the diagnostic performance remained sub
   - Status: external validation. Suggested key: `chang2026electrocardiogram`

3. **Deep learning-enabled ECG system for detecting left ventricular hypertrophy and predicting cardiovascular prognoses** (2026; PMID 41781965; DOI 10.1186/s13040-026-00536-2)
   - Type: external validation study. Modality: 12-lead ECG. Condition: atrial fibrillation / occult AF.
   - Scale/cohort: 40,736.
   - Why it matters: Left ventricular hypertrophy (LVH) is a common condition with a prevalence of 15%-20% in general population. Prior studies have suggested that deep learning model (DLM)-enabled electrocardiogram (ECG) systems can aid LVH detection and cardiovascular risk assessment; however, conventional manual ECG criteria have limited sensitivity and their prognostic utility remains suboptimal.
   - Status: external validation. Suggested key: `yang2026ecg`

4. **Detecting Transthyretin Cardiac Amyloidosis With Artificial Intelligence: A Nonrandomized Clinical Trial** (2026; PMID 41213043; DOI 10.1001/jamacardio.2025.4591)
   - Type: nonrandomized clinical trial. Modality: 12-lead ECG. Condition: hypertrophic cardiomyopathy.
   - Scale/cohort: 799.
   - Why it matters: ATTRACTnet was developed in an internal test set of 799 patients (mean [SD] age, 75.1 [11.1] years; 516 [64.7%] male and 283 [35.3%] female) using 5-fold cross-validation with an additional external test set of 422 patients. It had good discrimination for ATTR-CM detection with an area under the receiver operator characteristic curve of 0.85 (5-fold cross-validation, 0.77-0.85) in the internal set and 0.82 (95% CI, .
   - Status: external validation. Suggested key: `jain2026amyloidosis`

5. **ECG trained artificial intelligence for the detection of patients with inducible myocardial ischemia** (2026; PMID 41929849; DOI 10.1093/ehjdh/ztag050)
   - Type: external validation study. Modality: 12-lead ECG. Condition: coronary ischemia / acute chest pain.
   - Scale/cohort: 6070.
   - Why it matters: Aims Myocardial ischaemia is associated with adverse prognosis. Identifying high-risk individuals who require a stress test is challenging, and a practical screening tool to detect these patients, especially in asymptomatic individuals, is lacking.
   - Status: external validation. Suggested key: `lim2026ecg`

6. **Evaluation of artificial intelligence-based electrocardiogram analysis tools in patients with hypertrophic cardiomyopathy** (2026; PMID 41768038; DOI 10.1093/ehjdh/ztag026)
   - Type: implementation study. Modality: 12-lead ECG. Condition: hypertrophic cardiomyopathy.
   - Scale/cohort: 681.
   - Why it matters: Aims Artificial intelligence (AI)-based electrocardiogram (ECG) analysis tools have shown promise in detecting various cardiac conditions. However, their performance in specific patient populations, such as those with hypertrophic cardiomyopathy (HCM), remains incompletely characterized.
   - Status: observational/model-development study. Suggested key: `baburguler2026electrocardiogram`

7. **Improving transthyretin cardiac amyloidosis detection from electrocardiograms through the Willem artificial intelligence platform** (2026; PMID 41933633; DOI 10.1016/j.hrthm.2026.03.1949)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: cardiac amyloidosis.
   - Scale/cohort: 585.
   - Why it matters: In the test cohort, Willem AI achieved an area under the receiver operating characteristic curve (AUC) of 0.88 (95% confidence interval, 0.85-0.91), a sensitivity of 80.7%, and a specificity of 78.5%. Performance was similar for ATTRv (AUC, 0.91) and ATTRwt (AUC, 0.88) and remained informative in early presentations (asymptomatic sensitivity 68.4%; New York Heart Association class I 73.9%).
   - Status: retrospective derivation/validation. Suggested key: `gonzlezlpez2026amyloidosis`

8. **Old criteria, new intelligence: The evolution of ECG in pulmonary hypertension diagnosis** (2026; PMID 41544985; DOI 10.1016/j.rmed.2026.108646)
   - Type: implementation study. Modality: 12-lead ECG. Condition: pulmonary hypertension.
   - Why it matters: Traditional ECG criteria demonstrated consistently high specificity (71-100 %) but low sensitivity (0-66 %) for detection of PH, limiting screening utility while maintaining confirmatory value. AI-based algorithms achieved superior balanced diagnostic performance with sensitivity of 74-85 % and specificity of 85 %.
   - Status: review. Suggested key: `herreraleao2026ecg`

9. **A deep learning model could screen for coronary heart disease from a "pseudo-normal" electrocardiogram** (2025; PMID 40527801; DOI 10.1097/md.0000000000042764)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: coronary artery disease.
   - Scale/cohort: 15,995.
   - Why it matters: The model was developed using a dataset comprising 21,240 ECGs from 15,995 patients at SAH, with 4248 ECGs serving as the internal testing set. Additionally, 2572 ECGs from FAH were utilized as the external testing set.
   - Status: observational/model-development study. Suggested key: `zhang2025electrocardiogram`

10. **AI-ECG Supported Decision-Making for Coronary Angiography in Acute Chest Pain: The QCG-AID Study** (2025; PMID 40165577; DOI 10.3346/jkms.2025.40.e105)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: general cardiovascular screening.
   - Why it matters: This pilot study evaluates an artificial intelligence (AI)-assisted electrocardiography (ECG) analysis system, QCG, to enhance urgent coronary angiography (CAG) decision-making for acute chest pain in the emergency department (ED). We retrospectively analyzed 300 ED cases, categorized as non-coronary chest pain (Group 1), acute coronary syndrome (ACS) without occlusive coronary artery disease (CAD) (Group 2), and ACS
   - Status: retrospective derivation/validation. Suggested key: `park2025ecg`

11. **Advanced Diagnosis of Hypertrophic Cardiomyopathy with AI-ECG and Differences Based on Ethnicity and HCM Subtype** (2025; PMID 40649092; DOI 10.3390/jcm14134718)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: hypertrophic cardiomyopathy.
   - Scale/cohort: 404.
   - Why it matters: Background/Objective: Hypertrophic cardiomyopathy (HCM) often presents later in the disease course, with frequent misdiagnoses and population-level underdiagnoses. Underserved patients may have even greater diagnostic delays.
   - Status: retrospective derivation/validation. Suggested key: `lewontin2025ecg`

12. **External assessment of an artificial intelligence-enabled electrocardiogram for aortic stenosis detection** (2025; PMID 40703138; DOI 10.1093/ehjdh/ztaf067)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: aortic stenosis.
   - Scale/cohort: 5,425 patients.
   - Why it matters: External assessment of AI-ECG for aortic stenosis detection reported AUC about 0.85 with sensitivity 0.83, specificity 0.65, and NPV 0.94, making it attractive as a rule-out screen.
   - Status: external validation. Suggested key: `kim2025electrocardiogram`

13. **Artificial Intelligence-Enabled Electrocardiogram Improves the Diagnosis and Prediction of Mortality in Patients With Pulmonary Hypertension** (2022; PMID 36338407; DOI 10.1016/j.jacasi.2022.02.008)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: pulmonary hypertension.
   - Scale/cohort: 41,097 patients in development cohort.
   - Why it matters: AI-enabled ECG for pulmonary hypertension reported AUC 0.88 with sensitivity 81.0% and specificity 79.6%; predicted-positive patients had substantially higher long-term cardiovascular mortality.
   - Status: derivation plus prognostic validation. Suggested key: `liu2022electrocardiogram`

14. **Artificial Intelligence-Enhanced Electrocardiogram for the Early Detection of Cardiac Amyloidosis** (2021; PMID 34218880; DOI 10.1016/j.mayocp.2021.04.023)
   - Type: retrospective cohort/model development. Modality: wearable/single-lead ECG. Condition: cardiac amyloidosis.
   - Scale/cohort: not clearly extracted.
   - Why it matters: AI-ECG for cardiac amyloidosis achieved holdout AUC about 0.91 and identified many cases months before formal diagnosis, supporting latent disease detection from routine ECGs.
   - Status: retrospective derivation/validation. Suggested key: `grogan2021amyloidosis`

15. **Detection of Hypertrophic Cardiomyopathy Using a Convolutional Neural Network-Enabled Electrocardiogram** (2020; PMID 32081280; DOI 10.1016/j.jacc.2019.12.030)
   - Type: external validation study. Modality: 12-lead ECG. Condition: hypertrophic cardiomyopathy.
   - Scale/cohort: test cohort not stated in title metadata.
   - Why it matters: CNN-enabled ECG detection of hypertrophic cardiomyopathy reported test AUC about 0.96 with sensitivity 87% and specificity 90%, with particularly strong performance in younger patients.
   - Status: retrospective derivation/validation. Suggested key: `ko2020electrocardiogram`

## Implementation, deployment, and enabling methods

1. **AI-enabled electrocardiogram alert for potassium imbalance treatment: a pragmatic randomized controlled trial** (2026; PMID 41507124; DOI 10.1038/s41467-025-66394-4)
   - Type: pragmatic randomized controlled trial. Modality: 12-lead ECG. Condition: electrolyte imbalance.
   - Scale/cohort: 14,989.
   - Why it matters: Life-threatening dyskalemia, defined as an abnormal serum potassium concentration, is common in emergency settings that requires timely recognition and treatment and can be detected via AI-enabled electrocardiography. We conducted a pragmatic, open-label, randomized controlled trial with physician-level randomization to evaluate whether a real-time AI-enabled electrocardiography alert could improve physicians' manage
   - Status: randomized trial. Suggested key: `lin2026electrocardiogram`

2. **Detection of Hypokalemia, Hyponatremia, and Hyperkalemia in Heart Failure Patients Using Artificial Intelligence Techniques via Electrocardiography** (2026; PMID 41063616; DOI 10.5543/tkda.2025.18598)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: left ventricular systolic dysfunction / low EF.
   - Why it matters: The accuracy rates of the DLM in detecting hyponatremia, hypokalemia, and hyperkalemia were 83.33%, 95.33%, and 95.77%, respectively.
   - Status: observational/model-development study. Suggested key: `yign2026detection`

3. **Development and multicentre validation of an artificial intelligence electrocardiogram model for ventricular remodeling in repaired tetralogy of Fallot** (2026; PMID 41695565; DOI 10.1093/ehjdh/ztag015)
   - Type: implementation study. Modality: 12-lead ECG. Condition: left ventricular systolic dysfunction / low EF.
   - Why it matters: Aims Periodic cardiac MRI (CMR) is recommended to identify adverse ventricular remodelling in repaired tetralogy of Fallot (TOF), but access to CMR is uneven, and compliance is poor. We developed a 12-lead electrocardiogram (ECG) artificial intelligence (AI) biomarker to identify CMR-quantified adverse biventricular remodelling in repaired TOF.
   - Status: external validation. Suggested key: `duong2026electrocardiogram`

4. **External validation of ECG artificial intelligence for emergency and cardiac assessment across a large-scale U.S. healthcare system** (2026; PMID 42049841; DOI 10.1038/s41746-026-02682-7)
   - Type: external validation study. Modality: 12-lead ECG. Condition: pulmonary hypertension.
   - Scale/cohort: 1368.
   - Why it matters: An ECG-based artificial intelligence (AI) model was previously developed to generate ten digital biomarkers for emergency and cardiac assessment and is currently deployed in clinical practice in Korea (ECG Buddy, ARPI Inc.). Its external validity within U.S.
   - Status: external validation. Suggested key: `lee2026ecg`

5. **Real-Time Integration of an AI-Based ECG Interpretation System in the Emergency Department: A Pragmatic Alternating-Day Study of Diagnostic Performance and Clinical Process Metrics** (2026; PMID 41975970; DOI 10.3390/healthcare14070968)
   - Type: pragmatic implementation study. Modality: 12-lead ECG. Condition: general cardiovascular screening.
   - Scale/cohort: 1524.
   - Why it matters: Background/Objectives: Rapid and accurate electrocardiogram (ECG) interpretation is essential for timely recognition of ST-elevation myocardial infarction (STEMI) and initiation of reperfusion therapy in the emergency department (ED). We evaluated the diagnostic performance of a real-time artificial intelligence (AI) ECG interpretation system and its pragmatic impact when integrated into routine ED workflows.
   - Status: prospective/real-world evaluation. Suggested key: `choi2026ecg`

6. **Signal or noise? Evaluating commonly used attribution methods for explaining deep neural networks in electrocardiogram classification** (2026; PMID 41836589; DOI 10.1093/ehjdh/ztag038)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: general cardiovascular screening.
   - Why it matters: Aims Attribution-based explainability methods are widely used in electrocardiogram (ECG) analysis to interpret predictions from 'black-box' deep neural networks (DNNs). To be useful in clinical applications, attribution methods must produce explanations that are both clear and reflective of the model's inner workings.
   - Status: observational/model-development study. Suggested key: `arends2026electrocardiogram`

7. **A deep foundation model for electrocardiogram interpretation: enabling rare disease detection through transfer learning** (2025; PMID 40703125; DOI 10.1093/ehjdh/ztaf051)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: general cardiovascular screening.
   - Why it matters: In healthcare, scarcity of high-quality human-adjudicated labelled data may limit the potential of deep neural networks (DNNs). Foundation models provide an efficient starting point for deep learning that can facilitate effective DNN training with fewer labelled training examples.
   - Status: observational/model-development study. Suggested key: `hu2025electrocardiogram`

8. **A novel XAI framework for explainable AI-ECG using generative counterfactual XAI (GCX)** (2025; PMID 40604021; DOI 10.1038/s41598-025-08080-5)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: atrial fibrillation / occult AF.
   - Why it matters: Generative Counterfactual Explainable Artificial Intelligence (XAI) offers a novel approach to understanding how AI models interpret electrocardiograms (ECGs). Traditional explanation methods focus on highlighting important ECG segments but often fail to clarify why these segments matter or how their alteration affects model predictions.
   - Status: observational/model-development study. Suggested key: `jang2025ecg`

9. **Artificial Intelligence-Enabled Electrocardiogram for the Detection and Management of Cancer Therapy-Related Cardiotoxicity** (2025; PMID 41473234; DOI 10.1002/cai2.70042)
   - Type: retrospective cohort/model development. Modality: 12-lead ECG. Condition: cancer therapy-related cardiotoxicity.
   - Why it matters: Review of AI-ECG applications in cardio-oncology highlighting potential for earlier detection and management of therapy-related cardiotoxicity, with translation still dependent on prospective validation.
   - Status: review. Suggested key: `song2025electrocardiogram`

## Commercial and real-world deployment signals

1. **AliveCor Kardia 12L** (2026; https://alivecor.com/products/kardia12l)
   - Type: commercial / official product webpage. Modality: 12-lead ECG or ambulatory ECG workflow. Condition: commercial AI-ECG deployment.
   - Scale/cohort: 27,000+ patients; 250+ practices; 4,000+ instances of myocardial infarction and ischemia detected; AI trained with one million ECGs; 39 FDA-cleared determinations.
   - Why it matters: A commercial example of AI-enhanced ECG acquisition and interpretation packaged as a handheld 12-lead workflow product.
   - Status: official commercial source; independent validation still required. Suggested key: `alivecor2026commercial`

2. **Anumana ECG-AI** (2026; https://anumana.ai/ecg-ai/)
   - Type: commercial / official product webpage. Modality: 12-lead ECG or ambulatory ECG workflow. Condition: commercial AI-ECG deployment.
   - Scale/cohort: Commercial focus areas listed: low ejection fraction, pulmonary hypertension, cardiac amyloidosis; Workflow details include HL7 datapoints and CPT III code setup.
   - Why it matters: A strong enterprise AI-ECG example centered on disease-screening algorithms integrated into hospital ECG workflows.
   - Status: official commercial source; independent validation still required. Suggested key: `anumana2026commercial`

3. **Philips Cardiologs ECG analysis** (2026; https://www.philips.co.uk/healthcare/ambulatory-monitoring-and-diagnostics/ecg-monitoring/cardiologs-ecg-analysis)
   - Type: commercial / official product webpage. Modality: 12-lead ECG or ambulatory ECG workflow. Condition: commercial AI-ECG deployment.
   - Scale/cohort: Over 20 publications and abstracts; 4 patents; More than 200 million ECGs processed; Over two million patients diagnosed per year.
   - Why it matters: A scale-focused commercial AI-ECG/Holter interpretation platform embedded in ambulatory ECG workflows.
   - Status: official commercial source; independent validation still required. Suggested key: `philips2026commercial`
