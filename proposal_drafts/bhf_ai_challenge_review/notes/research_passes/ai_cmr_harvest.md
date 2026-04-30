# AI-CMR evidence harvest

## Scope and harvest summary

This pass focuses specifically on artificial intelligence and machine learning applied to cardiovascular magnetic resonance / cardiac MRI (CMR) for tasks that matter to a translational BHF programme: segmentation and quantification, diagnosis and phenotyping, fibrosis/scar assessment, prognosis and outcomes, workflow acceleration, and clinical validation.

Corpus produced here: **46 candidate citations** spanning reviews, technical methods, disease-specific diagnostic studies, large-scale population analyses, and outcome-focused models.

## High-level takeaways

1. **The most mature AI-CMR use case is automation of routine quantification.** Ventricular contouring, landmark detection, T1/T2 analysis, and perfusion preprocessing now show speed gains with accuracy near expert-level, and in some settings better precision than humans.
2. **Disease classification from CMR is becoming credible, especially for cardiomyopathy and amyloidosis.** The strongest recent paper is the 9,719-patient multi-disease Nature Medicine study showing scalable computerized CMR interpretation with internal and external validation (PMID 38740996).
3. **Scar and fibrosis are major opportunity areas.** AI is increasingly used to quantify HCM scar burden, infer fibrosis from non-contrast cine or mapping data, and scale myocardial T1 analyses to biobank-sized cohorts.
4. **Outcome prediction is promising but still mostly retrospective.** HCM, CAD, stress-CMR, and STEMI studies suggest real incremental value from CMR-derived AI features, but prospective impact studies are still scarce.
5. **Clinical translation remains the central weakness.** Most papers are retrospective, often single-center, with limited external validation, limited calibration reporting, and almost no implementation, health-economic, or randomized workflow evidence.

## Structured synthesis by theme

### 1) Segmentation, quantification, and workflow automation

This is the most mature and deployment-ready part of AI-CMR.

- Foundational reviews (PMIDs **31590664, 31111616, 31670597, 35628992, 38193835, 38925255, 40187819**) converge on the same point: AI reduces analysis time, improves reproducibility, and is likely to enter practice first through inline or near-inline automation.
- The strongest quantification paper is **Meyer et al.** (PMID **35272664**), which trained on **1,923 scans** and validated across multi-site datasets. It showed faster analysis (**20 seconds** versus **13 minutes**) and better scan-rescan precision than clinicians, with potential trial-efficiency gains.
- Practical workflow enablers include landmark detection (PMID **34617022**), T1/ECV quality-controlled automation (PMID **36827870**), automated T2 mapping validation (PMID **37869306**), perfusion preprocessing (PMID **31710769**), DENSE strain segmentation (PMID **36991474**), 4D-flow segmentation (PMID **38211658**), and free-running whole-heart 4D analysis (PMID **41453741**).
- Reconstruction and acquisition acceleration remain strategically important. Reviews on AI-based reconstruction and multi-contrast acceleration (PMIDs **32158767, 33966456**) support a workflow argument that AI-CMR can reduce bottlenecks before image interpretation even begins.

**BHF-relevant implication:** this is the safest translational entry point for a programme, because automation improves throughput, standardization, and data quality even before claiming new biology or treatment effects.

### 2) Diagnosis and phenotyping

AI-CMR is moving from “measurement automation” toward true disease interpretation.

- The standout paper is **Zhang et al.** (PMID **38740996**), a **9,719-patient** study covering **11 cardiovascular diseases**, with a two-stage cine-plus-LGE framework and strong external validation. This is one of the clearest signs that computerized CMR interpretation may become clinically scalable.
- Disease-specific classification is especially strong in **cardiomyopathy and amyloidosis**:
  - HCM / DCM / normal classification with radiomics (PMID **36378251**).
  - Multicenter differentiation of HCM versus AL and ATTR amyloidosis across **56 institutions** (PMID **40464070**).
  - LGE-based deep learning for cardiac amyloidosis (PMID **33287829**).
  - Non-contrast cine and mapping/radiomics approaches for amyloid versus HCM discrimination (PMIDs **36386316, 35597906, 34880319, 41188957**).
  - Automatic LV non-compaction diagnosis with strong segmentation-backed performance (PMID **34861618**).
- Myocarditis is promising but immature:
  - small DL classifier study (PMID **35240789**),
  - STIR radiomics to predict LGE (PMID **36116711**),
  - disease-focused review stressing that current evidence is underpowered and poorly controlled (PMID **39314764**).

**BHF-relevant implication:** AI-CMR is no longer only about contours. There is now credible evidence for disease phenotyping and differential diagnosis, particularly in cardiomyopathy pathways where MRI is already central.

### 3) Fibrosis and scar

Fibrosis/scar is one of the highest-value domains because it links CMR tissue characterization to risk and treatment decisions.

- In HCM, scar-focused work is already substantial:
  - automated scar quantification on LGE (PMID **36812626**),
  - cine-based screening to identify patients unlikely to have scar before gadolinium administration (PMID **35761339**).
- Mapping-based radiomics extends this toward **non-contrast fibrosis phenotyping**, especially for amyloid/HCM differentiation and phenotype classification (PMIDs **34880319, 36386316, 35597906, 41188957**).
- At population scale, machine learning-derived T1 analyses are especially influential:
  - myocardial interstitial fibrosis genetics in **41,505 UK Biobank** participants (PMID **37081215**),
  - multi-organ fibrosis in **43,881** participants with mortality associations (PMID **38806679**).
- Quality-controlled automation for T1/ECV (PMID **36827870**) is important because fibrosis pipelines are otherwise highly vulnerable to silent segmentation failure.

**BHF-relevant implication:** fibrosis/scar is a particularly compelling bridge from imaging AI to biological mechanism, prognosis, and treatment selection. It is also a strong fit with cardiomyopathy, post-MI remodeling, and potentially atrial disease workstreams.

### 4) Prognosis, outcomes, and decision support

Outcome-focused AI-CMR is increasingly strong, although still mostly retrospective.

- **Stress-CMR / CAD**
  - ML survival modeling using stress perfusion CMR plus clinical data (PMID **35987738**).
  - Deep-learning-based epicardial adipose tissue quantification improved MACE prediction in **730** stress-CMR patients, with derivation and validation cohorts (PMID **38679562**).
  - Automated strain from stress CMR in **2,778** patients independently improved event prediction (PMID **40948124**).
  - Multimodal CCTA + stress CMR ML in **2,038** obstructive CAD patients achieved **AUC 0.86** with two external validation datasets (PMID **39807980**).
- **HCM**
  - Clinical + CMR ML risk model in **758** patients outperformed HCM Risk-SCD for broader cardiovascular events (PMID **39001729**).
  - The multimodal MAARS model forecast arrhythmic death better than current guidelines, with internal and external validation (PMID **40603582**).
- **Post-MI / STEMI**
  - DeepSTEMI used multisequence CMR plus clinical inputs, developed in **610** registry patients and externally validated in **334** more, reaching **AUC 0.894** for 2-year MACE prediction (PMID **41314962**).

**BHF-relevant implication:** there is now enough evidence to justify an AI-CMR work package focused on clinically meaningful outcomes, but proposals should avoid implying that purely retrospective AUC gains are already practice-changing.

### 5) Clinical validation and readiness for deployment

The evidence base is strongest where AI helps standardize existing CMR workflows, and weakest where it claims direct decision superiority.

**What looks mature enough for near-term translation**
- ventricular segmentation/quantification
- landmark detection and planning support
- mapping automation with explicit QC
- perfusion preprocessing and strain extraction
- selective disease-screening tools in high-pretest-probability pathways

**What still looks early or fragile**
- myocarditis classification from small retrospective datasets
- many radiomics studies with internal-only validation
- non-contrast fibrosis inference without prospective outcome testing
- broad automated diagnosis claims without implementation studies in real NHS workflows

**Common recurrent gaps across the corpus**
- retrospective design dominates
- few prospective or randomized workflow studies
- external validation is inconsistent
- calibration, subgroup fairness, and failure-mode reporting are often thin
- manual labels remain the ground truth, so many papers measure agreement with experts rather than clinical benefit
- limited evidence on health economics, regulatory readiness, and model maintenance/drift

## Most useful citations for a BHF proposal narrative

If the proposal needs a compact, high-yield evidence spine, the most useful anchor papers are:

1. **PMID 38740996**: large-scale AI-enabled CMR screening/diagnosis across 11 CVDs.
2. **PMID 35272664**: automated quantification with better-than-human precision for routine structure/function measurement.
3. **PMID 40464070**: multicenter amyloid/HCM differentiation, strong example of disease-focused CMR AI with wide institutional diversity.
4. **PMID 36812626** and **35761339**: scar-focused HCM work, directly relevant to fibrosis/scar-based stratification.
5. **PMID 37081215** and **38806679**: scaling fibrosis quantification to biobank and mechanism-discovery settings.
6. **PMID 39001729** and **40603582**: HCM outcomes and arrhythmic risk, showing the route from CMR features to clinical decision support.
7. **PMID 39807980**, **40948124**, and **41314962**: outcome-focused translational studies in CAD/stress CMR and STEMI.
8. **PMID 36827870** and **37869306**: practical examples of QC-aware mapping automation, important for trustworthy deployment.

## Bottom line for the BHF review

AI-CMR is no longer a niche image-processing topic. The literature now supports a credible programme-level narrative in which AI improves:

- **throughput and standardization** of CMR analysis,
- **disease phenotyping and differential diagnosis**, especially in cardiomyopathy pathways,
- **fibrosis/scar quantification** and tissue characterization,
- **risk stratification** for clinically meaningful outcomes,
- and potentially **contrast-sparing or protocol-shortening workflows**.

The strongest gap, and therefore the strongest opportunity for a BHF programme, is not another single-center classifier. It is a **prospective, multicenter, clinically embedded validation programme** that links AI-CMR outputs to patient pathways, safety, equity, implementation, and outcome impact.
