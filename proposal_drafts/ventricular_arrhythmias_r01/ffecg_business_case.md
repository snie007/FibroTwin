# Literature-evidenced business case for ffECG

## Framing question
Why would a clinical or translational electrophysiology program want an ffECG system?

## Short answer
The strongest literature-based case is not that ffECG is already proven to improve outcomes. It is that ventricular tachycardia (VT) ablation and cardiac resynchronization therapy (CRT) involve high-stakes decisions, that current workflows have important limitations, and that patient-specific computational approaches are being explored as a way to add useful mechanistic information. A validated ffECG system could therefore be valuable if it adds patient-specific mechanistic information beyond current workflows. That is the defensible business case today. It is a decision-support case, not yet a proven outcomes case.

## 1) The clinical problem is large enough to matter

### Ventricular arrhythmia and sudden death are important clinical burdens
- Ventricular arrhythmias are described as an important cause of morbidity and mortality, and catheter ablation is a central part of contemporary management in appropriate patients [PMID: 31075787].
- Sudden cardiac death accounts for roughly 300,000 to 400,000 deaths annually in the United States, with most sudden cardiac deaths being cardiac and commonly related to arrhythmias associated with structural heart disease or primary electrical abnormalities [PMID: 25813838].

### The heart-failure and CRT population is also large
- A review cited in the local ffECG library states that 5.7 million adults in the United States suffer from heart failure and that almost 50% of patients diagnosed with heart failure die within 5 years of diagnosis [PMID: 29173412].
- Cardiac physiologic pacing, including CRT and conduction system pacing, is now guideline-framed as a strategy that may mitigate or prevent heart failure in patients with ventricular dyssynchrony or pacing-induced cardiomyopathy [PMID: 37283271].
- Despite established indications, CRT has been underused in the United States, with many patients receiving implantable cardioverter-defibrillators who could benefit from appropriately indicated CRT but are not receiving it [PMID: 24948569].

## 2) Current tools are useful, but they leave major decision gaps

### VT ablation still relies on imperfect and invasive workflows
- Mapping and ablation of ventricular arrhythmias in cardiomyopathies remain a major challenge. Electroanatomic abnormalities are often inaccessible to conventional endocardial ablation, and detailed electroanatomic mapping plus advanced imaging are needed to guide strategy [PMID: 31706471].
- In scar-related VT, clinicians often need a combination of substrate mapping, activation mapping, pace mapping, and entrainment mapping to identify ablation targets [PMID: 28167086].
- MRI-based scar characterization can help identify conduction channels and deceleration zones that are relevant to VT ablation planning [PMID: 38262674; PMID: 36607130].

### CRT guidance also remains incomplete
- Conventional biventricular pacing benefits many patients, but therapeutic success is widely variable and is limited by myocardial scar, fibrosis, and inability to effectively stimulate diseased tissue [PMID: 35715087].
- A 2023 network meta-analysis reported that biventricular CRT is ineffective in approximately one-third of patients [PMID: 37767743].
- A review focused on CRT non-response states that the non-response rate of approximately 30% has remained nearly unchanged for decades, even though non-invasive electrical mapping methods may help predict response before implantation [PMID: 31094217].
- Newer electrical metrics such as QRS area are promising, but their clinical use remains unclear rather than settled standard of care [PMID: 35000207].

## 3) Why existing non-invasive electrical mapping is not enough on its own
- ECGi is attractive because it can reconstruct activation from a single beat using body-surface electrodes and imaging-derived geometry [PMID: 34777827].
- But inverse ECG reconstruction is fundamentally difficult because reconstructing cardiac electrophysiology from remote body-surface measurements is a highly ill-posed problem [PMID: 15649241].
- In human studies, ECGi accuracy has varied. The literature note in the local library states that more recent work suggests only moderate accuracy and that ECGi is likely not accurate enough to guide more discrete radiofrequency ablation, even if it may be sufficient for larger treatment targets such as non-invasive radioablation planning [PMID: 34777827].

## 4) Where ffECG could create real value if validated

The most defensible value proposition is that ffECG could be developed as an additional non-invasive decision-support layer alongside routine ECG, imaging, and invasive assessment where needed.

### A. VT ablation planning
A center would want ffECG if it could non-invasively generate a patient-specific mechanistic hypothesis before the case begins, for example by helping localize abnormal activation or likely substrate regions that deserve focused invasive testing. This use case is most plausible in VT because ablation is important, difficult, and still dependent on complex invasive workflows [PMID: 31075787; PMID: 31706471]. The literature on CMR-identified channels and slow-conduction targets shows that better pre-procedure substrate definition is clinically relevant in this setting [PMID: 38262674; PMID: 36607130].

### B. CRT and conduction-system pacing selection or optimization
A center would want ffECG if it could improve pre-implant stratification or pacing-strategy selection in a setting where current response is variable and current selection markers are incomplete. This use case is plausible because CRT is clinically important, underused, and still has a persistent non-responder group [PMID: 24948569; PMID: 35715087; PMID: 37767743; PMID: 31094217].

### C. A more integrated interpretation layer
A center would want ffECG if it could combine information that is usually interpreted separately, namely body-surface electrical data, cardiac imaging, and mechanistic prior knowledge. Reviews of computational cardiology argue that patient-specific models have the potential to improve understanding of arrhythmia drivers, personalize treatment plans, and support resynchronization therapy planning [PMID: 33303478; PMID: 38323181].

## 5) Why a computational decision-support system is a plausible direction
- Reviews in computational cardiology state that patient-specific models built from clinical imaging have the potential to tailor understanding of arrhythmia mechanisms, estimate risk, and personalize treatment planning [PMID: 33303478].
- Broader cardiovascular modelling reviews argue that computational models may provide non-invasive indicators and support diagnosis, treatment planning, and follow-up testing [PMID: 38323181].
- The local ffECG evidence map also highlights an important caution: uncertainty quantification and model discrepancy matter when using mechanistic models for decisions, so a serious ffECG platform should include calibration and uncertainty awareness rather than a single deterministic answer [PMID: 32448065].

## 6) The most defensible buyer-side argument today
If I strip this down to the shortest evidence-based commercial logic, it is this:

1. There are high-burden patient groups in VT and heart failure / CRT where decision quality matters a great deal [PMID: 31075787; PMID: 25813838; PMID: 29173412; PMID: 37283271].
2. Current tools remain incomplete. VT planning is invasive and difficult, CRT response remains variable, and ECGi alone has important inverse-problem limitations [PMID: 31706471; PMID: 35715087; PMID: 37767743; PMID: 15649241; PMID: 34777827].
3. There is literature support for patient-specific computational methods as a clinically relevant direction, especially for arrhythmia treatment planning and resynchronization therapy [PMID: 33303478; PMID: 38323181].
4. Therefore, a non-invasive system in this category could be worth adopting if it demonstrates incremental value over current workflow.

In plain language: you would want one of these systems if it helps you make a better decision before you put a catheter in the patient or before you commit the patient to a pacing strategy.

## 7) Claims that are not justified yet, and should not be made
To avoid hallucination or overstatement, the current literature does **not** justify saying that ffECG:
- already improves hard clinical outcomes,
- already reduces procedure time or cost,
- can replace invasive electroanatomic mapping,
- can robustly identify all relevant substrate in every patient,
- is already proven superior to ECGi or conventional planning in prospective trials.

Those are future validation questions, not current evidence-backed claims.

## 8) Bottom-line business case
The literature-backed business case for ffECG is strongest when positioned as a **mechanism-oriented, non-invasive decision-support layer** for high-value electrophysiology decisions, especially VT ablation planning and CRT / conduction-system pacing selection or optimization. The need is real, current tools have material limitations, and the computational-modelling literature supports this as a plausible direction for development. The honest commercial position is that ffECG should be developed and evaluated as a tool to improve pre-procedure understanding and patient-specific planning, not marketed as a proven replacement for invasive mapping or as an outcomes-improving product until prospective evidence exists.

## Source notes used for this draft
- `paper_library/notes/PMID-31075787_2019_HRS_EHRA_APHRS_LAHRS_expert_consensus_statement_on_catheter_ablation_of_ventricular_a.md`
- `paper_library/notes/PMID-25813838_Sudden_cardiac_death.md`
- `paper_library/notes/PMID-29173412_Heart_Failure_and_Sudden_Cardiac_Death.md`
- `paper_library/notes/PMID-37283271_2023_HRS_APHRS_LAHRS_guideline_on_cardiac_physiologic_pacing_for_the_avoidance_and_mitigat.md`
- `paper_library/notes/PMID-24948569_On_the_underutilization_of_cardiac_resynchronization_therapy.md`
- `paper_library/notes/PMID-31706471_Mapping_and_Ablation_of_Ventricular_Arrhythmias_in_Cardiomyopathies.md`
- `paper_library/notes/PMID-28167086_Entrainment_Mapping.md`
- `paper_library/notes/PMID-38262674_Non_invasive_detection_of_slow_conduction_with_cardiac_magnetic_resonance_imaging_for_vent.md`
- `paper_library/notes/PMID-36607130_Scar_conducting_channel_characterization_to_predict_arrhythmogenicity_during_ventricular_t.md`
- `paper_library/notes/PMID-35715087_Conduction_System_Pacing_for_Cardiac_Resynchronization_Therapy.md`
- `paper_library/notes/PMID-37767743_Effectiveness_of_conduction_system_pacing_for_cardiac_resynchronization_therapy_A_systemat.md`
- `paper_library/notes/PMID-31094217_Non_invasive_cardiac_mapping_for_non_response_in_cardiac_resynchronization_therapy.md`
- `paper_library/notes/PMID-35000207_QRS_area_as_a_predictor_of_cardiac_resynchronization_therapy_response_A_systematic_review_.md`
- `paper_library/notes/PMID-34777827_The_Use_of_Electrocardiographic_Imaging_in_Localising_the_Origin_of_Arrhythmias_During_Cat.md`
- `paper_library/notes/PMID-15649241_Challenges_facing_validation_of_noninvasive_electrical_imaging_of_the_heart.md`
- `paper_library/notes/PMID-33303478_Translational_applications_of_computational_modelling_for_patients_with_cardiac_arrhythmia.md`
- `paper_library/notes/PMID-38323181_The_role_of_computational_methods_in_cardiovascular_medicine_a_narrative_review.md`
- `paper_library/notes/PMID-32448065_Considering_discrepancy_when_calibrating_a_mechanistic_electrophysiology_model.md`
