# Background literature review for the BHF AI challenge concept

Note: direct access to the Overleaf project was blocked during collection, so this review is based on the preliminary abstract plus publicly accessible call documents, guidelines, publications, and commercial webpages saved locally in this workspace.

## Core proposition being tested

The draft idea is strongest when framed as a move away from static cardiovascular risk prediction and toward *individualized decisions over time*:

1. individual treatment effect estimation, not just average-risk prediction
2. latent disease-trajectory modelling, not one-off cross-sectional classification
3. multimodal fusion across ECG, imaging, EHR, genetics, and wearables
4. clinically safe escalation and de-escalation rules, especially where negative predictive value matters

The three proposed anchors still make sense because they represent three different decision types:

- *AF ablation* = who is likely to benefit enough from an invasive rhythm-control strategy
- *cardiomyopathy family screening* = who needs closer versus lighter surveillance
- *post-MI care* = who needs more intensive follow-up, treatment optimization, or rehabilitation attention over time

---

## 0) Broader studies on this kind of idea

### A. The precision-cardiovascular-AI literature is real, but still mostly prediction-heavy

A 2023 scoping review of AI-based precision cardiovascular medicine included *28 studies* and found that the field was still dominated by *prediction (50%)*, with less work in *diagnosis (21%)*, *phenotyping (14%)*, and *risk stratification (14%)*. Most studies used *EHR data (79%)*, with imaging in *43%*. PMID: *37623518*.

That matters because the proposal is trying to move one step beyond the current center of gravity. It is not enough to predict risk. The harder and more interesting question is how to use longitudinal multimodal data to change decisions.

### B. Dynamic treatment-regime methods are now a recognized clinical-AI direction

A 2025 systematic review of reinforcement learning in precision medicine and dynamic treatment regimes included *46 studies* and reported a sharp rise since 2020, but also emphasized persistent barriers around:

- interpretability
- reward definition
- data limitations
- clinician adoption

PMID: *40724777*.

So the idea is timely, but reviewers will expect very careful language around causal assumptions, policy learning, and guardrails.

### C. Cardiovascular digital-twin thinking is adjacent, but can easily become too futuristic

A 2024 *European Heart Journal* review described cardiovascular digital twins as systems that integrate multimodal data into mechanistic and statistical models to improve disease phenotyping, diagnostic workflows, and procedural planning. PMID: *39322420*.

This is useful background because it shows that the field is already converging on:

- multimodal fusion
- individualized simulation
- dynamic updating
- procedural decision support

But it is also a warning. If the proposal sounds like speculative digital-twin futurism, it may lose BHF reviewers. The safer framing is decision-grade longitudinal modelling with explicit validation and implementation plans.

### D. Post-MI AI has broader evidence than the first-pass review captured

A 2025 systematic review and meta-analysis of machine-learning models for *major cardiovascular events after MI* included *28 studies* covering *59,392 patients* and reported pooled validation performance of:

- *C-index 0.77* (95% CI 0.74 to 0.81)
- sensitivity *0.78*
- specificity *0.85*

PMID: *40630448*.

This is helpful because it strengthens the post-MI arm. The field is not empty. The gap is that most models remain early event-prediction tools rather than longitudinal treatment and follow-up policies.

---

## 1) AI-ECG review: academic and commercial

## A. Academic AI-ECG literature

### 1. AI-ECG has already shown that cheap physiology can encode latent structural disease

The landmark low-EF screening paper trained on *44,959* patients and tested on *52,870*, achieving:

- *AUC 0.93*
- sensitivity *86.3%*
- specificity *85.7%*

Among patients without ventricular dysfunction, a positive AI-ECG screen was associated with *4.1-fold* higher risk of later ventricular dysfunction. PMID: *30617318*.

That is exactly the kind of result that makes AI-ECG relevant to this proposal. It suggests routine ECG can carry a longitudinal latent-state signal, not just present-time rhythm information.

### 2. AI-ECG has broadened beyond rhythm classification

Important disease-specific examples now include:

- *AF during sinus rhythm*: *180,922* patients, *649,931* sinus-rhythm ECGs, AUC *0.87* from a single ECG and *0.90* when multiple ECGs were used. PMID: *31378392*.
- *HCM detection*: test AUC *0.96*, sensitivity *87%*, specificity *90%*, with especially strong performance in younger patients. PMID: *32081280*.
- *Cardiac amyloidosis*: holdout AUC *0.91*, with *84%* of amyloidosis cases detected, and prediction more than *6 months* before diagnosis in *59%* of those with prediagnosis ECGs. PMID: *34218880*.
- *Pulmonary hypertension*: development cohort *41,097* patients, AUC *0.88*, sensitivity *81.0%*, specificity *79.6%*, with a *6-year* cardiovascular mortality HR of *3.69* for those predicted positive. PMID: *36338407*.
- *Aortic stenosis external validation*: *5,425* patients, AUC *0.85*, sensitivity *0.83*, specificity *0.65*, NPV *0.94*. PMID: *40703138*.

Together, these papers show that AI-ECG is no longer just an arrhythmia story. It is increasingly a low-cost screen for latent structural and hemodynamic phenotypes.

### 3. The strongest AI-ECG papers also point toward uncertainty-aware and longitudinal use

A 2022 study on AI-ECG for low EF added an explicit confidence estimate. With low-confidence cases excluded, performance improved from:

- internal AUC *0.9549* to *0.9759*
- external AUC *0.9365* to *0.9653*

A positive high-confidence AI-ECG was associated with *8.67-fold* higher future LV dysfunction risk. PMID: *36532114*.

This is especially relevant for the BHF proposal because it matches the stated interest in *safe de-escalation*. If the system cannot quantify uncertainty, it will be much harder to justify lighter surveillance or non-intervention.

### 4. External validation and reproducibility are still major weaknesses

A 2023 systematic review found *53* clinically relevant ECG deep-learning models across *44* manuscripts, but only:

- *18/53 (34%)* had external validation
- *10/44 (23%)* gave enough detail for reproduction
- *5/44 (11%)* made code or implementation resources available

PMID: *38288263*.

A 2024 external validation of an existing LVSD model still looked good overall, AUROC *0.88*, sensitivity *82%*, specificity *77%*, but performance was worse in tachycardia, AF, and wide-QRS subgroups. PMID: *38505486*.

A 2025 meta-analysis of ECG-based AI for heart-failure prediction included *11 cohorts* and *1,728,134 participants*, but pooled performance was only *0.76* with *high heterogeneity* (*I2 = 89%*), and the authors explicitly noted lack of clinical-validity evidence. PMID: *41552681*.

So the right take is not "AI-ECG is solved." It is:

- clinically impressive in some use cases
- increasingly scalable
- still quite uneven in external transportability and reporting quality

### 5. How AI-ECG should be used in this proposal

The best way to use AI-ECG here is *not* to turn the whole BHF application into an AI-ECG proposal.

It works better as:

- a low-cost longitudinal phenotyping layer
- a scalable rule-out or trigger modality
- a gateway into richer imaging/genetic/EHR assessment
- an NHS-friendly modality because ECG is already ubiquitous

That positioning fits AF, cardiomyopathy, and post-MI much better than presenting AI-ECG as a standalone destination.

## B. Commercial AI-ECG offerings

Important commercial signals, based on locally saved product pages, include:

### 1. AliveCor Kardia 12L

AliveCor describes Kardia 12L as an *"FDA-cleared ... AI-powered handheld 12-lead resting ECG system"* and reports:

- *27,000+ patients*
- *250+ practices*
- *4,000+ instances of myocardial infarction and ischemia detected*
- AI trained with *one million ECGs*
- *39 FDA-cleared determinations*

Source: `docs/raw/webpages/alivecor-kardia12l.html`.

This is important because it shows a commercial pathway centered on easier ECG acquisition plus onboard AI interpretation.

### 2. Anumana ECG-AI

Anumana positions ECG-AI as enterprise disease screening from standard 12-lead ECGs and prominently advertises *"First and Only FDA Clearance for ECG-AI Cardiac Amyloidosis Algorithm Using a Standard 12-Lead ECG"*. The page also highlights commercial targets in:

- low ejection fraction
- pulmonary hypertension
- cardiac amyloidosis

and workflow plumbing such as:

- HL7 datapoints
- ECG-management-system integration
- CPT III code setup

Source: `docs/raw/webpages/anumana-ecg-ai.html`.

This is the clearest example of AI-ECG as a hospital-integrated screening product rather than a research prototype.

### 3. Philips Cardiologs

Philips describes Cardiologs as the *"first FDA-cleared ECG analysis solution powered by deep learning technology"* and reports:

- *over 20 publications and abstracts*
- *4 patents*
- *more than 200 million ECGs processed*
- *over two million patients* diagnosed per year

Source: `docs/raw/webpages/philips-cardiologs-ecg-analysis.html`.

This points to another commercial lane: AI-ECG not just for disease screening, but for service-line scale, ambulatory interpretation, and workflow efficiency.

### Commercial take-home

Commercial AI-ECG is already a real market category. But the evidence is mixed in type:

- academic literature gives disease-level performance estimates
- commercial pages emphasize scale, regulatory status, workflow integration, and product claims

That combination supports including AI-ECG in the proposal, but only with very explicit external-validation and NHS-evaluation plans.

---

## 2) Broader review of LLM use for guiding or informing procedures

The most important finding here is that the literature is broader than I first captured, but it is still mostly about *support around procedures*, not autonomous procedural guidance.

### A. The strongest current use cases are education, consent, documentation, and checklist-style support

Examples:

- *Preoperative patient education in anesthesiology*: *30* standardized questions, *5* LLMs, *5* senior anesthesiology professors as raters. LLMs looked usable as support tools, but performance varied significantly by model and topic. PMID: *41899118*.
- *Interventional-radiology patient leaflets*: readability improved from grade *11.1* to *9.5* after LLM rewriting, but still did not reach the recommended grade *6*. PMID: *41052822*.
- *IR consent-process information*: GPT-4 outputs were rated highly for readability and tone, but only *67%* of physicians were comfortable giving the outputs directly to patients. PMID: *39612047*.
- *LLM-based consent documentation vs surgeon-generated text*: across *6* procedures and *36* RBA documents, LLM text had better composite completeness and accuracy scores and better readability. PMID: *37812419*.

So, LLMs can already help *inform* procedures, especially around patient communication and standardization.

### B. Perioperative safety support looks promising, but the evidence is mostly synthetic or vignette-based

A 2026 study of perioperative drug interaction detection used *40* synthetic vignettes and found that ChatGPT correctly identified *76 of 80* clinically significant interactions, sensitivity *95%*. PMID: *41952934*.

Encouraging, yes. But this is still far from live, accountable perioperative decision support.

### C. Procedure selection is much harder than coarse triage

In minimally invasive spine surgery, two advanced LLMs showed only slight-to-fair agreement on detailed procedural categories, but much better agreement when the task was collapsed to *surgical versus non-surgical triage*. PMID: *41424195*.

That distinction is very important. It suggests that LLMs may help with:

- sorting
- summarizing
- surfacing options
- drafting explanations

but should not be treated as reliable procedure-selection engines.

### D. The workflow is already arriving before the governance

A 2026 national OMFS resident survey found:

- *79.0%* had used an LLM
- *51.9%* used them at least monthly
- *97.5%* had received no formal LLM education in residency

PMID: *41721118*.

So even if the proposal barely mentions LLMs, reviewers should assume clinicians and trainees are already using them informally.

### E. Systematic reviews are still cautious

A 2025 systematic review in anesthesiology and critical care included *45 papers* and concluded that LLMs are *not yet equipped to fully assist physicians*, even though they have significant potential in patient education, simple scenario handling, and perioperative support. PMID: *40524117*.

A 2026 systematic review in cardiology found promise in education and ECG interpretation, but highlighted inconsistency in emergency guidance and readability, and a heavy reliance on small in silico studies. PMID: *41989882*.

### F. Citation reliability is a real safety issue

A 2024 orthopaedic-trauma paper found that among *30* ChatGPT-4-generated references, only *43.3%* were accurate, while *56.7%* were inaccurate or nonexistent. PMID: *39238880*.

That is directly relevant to this proposal because it means any LLM-supported procedure summaries, evidence notes, or consent materials would need hard verification layers.

### LLM take-home

For this proposal, LLMs make sense only in a subordinate role:

- patient explanation
- consent-support drafting
- MDT summarization
- procedure-prep information
- documentation assistance

They do *not* yet have a strong evidence base for autonomous or near-autonomous procedure guidance.

---

## 3) Five-perspective synthesis

## A. Clinical perspective

### AF ablation remains the best treatment-effect heterogeneity case

*CABANA* remains the cleanest starting point.

- Primary endpoint: *8.0%* with ablation versus *9.2%* with drugs, HR *0.86* (95% CI 0.65 to 1.15)
- Death or cardiovascular hospitalization: *51.7%* versus *58.1%*, HR *0.83* (95% CI 0.74 to 0.93)
- AF recurrence: *49.9%* versus *69.5%*, HR *0.52* (95% CI 0.45 to 0.60)

PMID: *30874766*.

The newer comorbidity analysis is especially valuable because it gives an explicit heterogeneity signal:

- high comorbidity burden HR *0.62* (95% CI 0.42 to 0.93)
- low comorbidity burden HR *1.16* (95% CI 0.76 to 1.77)
- interaction *P = 0.038*

PMID: *41213867*.

That is almost tailor-made for a proposal on individualized treatment effect estimation.

### Multimodal phenotyping already matters clinically

In *DECAAF*, recurrent arrhythmia at day 475 increased from *15.3%* in stage-1 fibrosis to *69.4%* in stage-4 fibrosis, and every *1%* increase in fibrosis increased recurrence hazard by *1.06*. PMID: *24496537*.

The clinical message is simple: the proposal is more believable if multimodal phenotyping is treated as essential, not ornamental.

### Cardiomyopathy family screening gives the strongest surveillance-intensity use case

For DCM relatives, *14.1%* of *1,365* first-degree relatives had new DCM-related findings, including *2.1%* DCM. PMID: *37225358*.

For HCM relatives, baseline yield was high but repeated follow-up yield was much lower:

- baseline combined clinical/genetic yield *26%*
- only *43* additional HCM diagnoses over *6,762 person-years*
- only *0.4%* conversion in one very-low-risk gene-elusive subgroup

PMID: *39365224*.

That is exactly the niche where trajectory-informed de-escalation could matter.

### Post-MI now has a stronger evidence footing

The first-pass review understated how much broader post-MI AI evidence already exists:

- NICE NG185 explicitly covers early and longer-term rehabilitation management
- a 2025 ischemia review included *30* studies, PMID *41523481*
- a 2025 post-MI MACE meta-analysis included *28* studies and *59,392* patients, PMID *40630448*
- a 2026 STEMI mortality model reached AUC *0.821* with only *5* features, PMID *41688111*

So the post-MI case is now stronger. The gap is still dynamic care optimization, not mere event prediction.

## B. Engineering perspective

The engineering novelty should be framed as the combination of three hard problems:

1. heterogeneous treatment effect estimation
2. latent temporal-state modelling under irregular follow-up
3. multimodal fusion with explicit missingness, uncertainty, and transportability handling

The deeper review also sharpens two supporting claims:

- *AI-ECG* shows that cheap, widely available signals can encode latent cardiovascular phenotype
- *LLMs* show promise mainly at the interface layer, not as the clinical core

That leads to a tighter stack:

- *core scientific engine*: longitudinal multimodal decision models
- *scalable ingress layer*: ECG and other low-friction signals where useful
- *communication/workflow layer*: clinician-supervised LLM tools for explanation and documentation only

## C. Grant reviewer perspective

The proposal now has a clearer answer to "why this, why now?"

- the methodology is more mature than a purely speculative idea
- the clinical use cases are distinct but unifiable
- AI-ECG offers an NHS-scalable entry modality
- commercial products prove translational demand exists
- the LLM evidence argues for a narrow, realistic adjunct role rather than hype

The main reviewer anxieties will still be:

- too many ideas under one roof
- overclaiming causal treatment optimization from observational data
- turning AI-ECG into a disconnected side-show
- letting LLMs sound more clinically mature than they are

## D. Patient perspective

The existing patient-preference result remains central: in heart-failure patients, only *18.2%* were comfortable with AI acting without physician input, while *97.3%* would trust their cardiologist over AI in disagreement. PMID: *41346424*.

The newer LLM literature fits that perfectly. Patients may benefit from:

- clearer procedure information
- more readable documents
- standardized consent-support materials

But that is still consistent with a clinician-supervised model rather than automation.

## E. Policy expert perspective

The policy environment remains receptive but conditional:

- NICE ESF wants evidence proportionate to risk and function
- MHRA and FDA both emphasize lifecycle governance for adaptive software
- commercial AI-ECG shows that workflow integration and reimbursement logic matter
- LLM evidence is still too immature for strong clinical-decision claims without prospective oversight

This means the proposal should explicitly separate:

- decision models that may become regulated decision-support tools
- communication/documentation aids that need governance but may sit at a different regulatory intensity

---

## 4) Tightened recommendation for the proposal write-up

### What to emphasize

- One *generalizable decision platform*, not three disease silos
- Clinical questions about *who benefits, who needs surveillance, and who can safely avoid extra intervention*
- Multimodal longitudinal modelling as the scientific core
- AI-ECG as a pragmatic, scalable phenotyping/input layer
- LLMs only as a supervised interface and workflow layer
- NHS-facing validation, governance, fairness, and implementation from day 1

### What to de-emphasize

- generic "AI will transform cardiology" language
- futuristic digital-twin rhetoric without a concrete validation plan
- any implication of autonomous LLM-guided procedures
- any tendency to let AI-ECG become a fourth unrelated mini-project

### Recommended tighter one-line thesis

*This programme will move cardiovascular AI from static risk prediction toward individualized decisions about intervention, surveillance, and follow-up intensity, using multimodal longitudinal data, scalable physiological signals such as ECG, and explicitly NHS-ready evidence generation.*

### Recommended tighter reviewer-facing contrast sentence

*This is not another cardiovascular prediction-score proposal: it is a programme to decide who benefits from treatment, who requires closer surveillance, and who can be safely spared unnecessary follow-up, with validation designed for clinical practice rather than benchmark performance alone.*
