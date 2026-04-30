# Tailoring notes for the BHF Cardiovascular Grand Challenge AI theme

## What the call clearly rewards

From the guidance and FAQ, the proposal should read as:

- *timely and ambitious*
- a *transformative advance rather than incremental progress*
- a *large integrated programme*, not a bundle of small studies
- clinically important and clearly translatable
- strongly governed, patient-involving, and NHS-legible

Key hard facts:

- award size: *up to £10 million over 5 years*
- outline deadline: *05 August 2026*
- full application: *March 2027*
- interviews: *June 2027*
- formal review after *year 1*
- *smaller standalone projects are unlikely to be competitive*

## Recommended framing

### 1. Present one platform, not three diseases

Best framing:

- *Generalizable AI framework for dynamic, individualized cardiovascular decision-making*
- demonstrated in 3 use-cases with different decision types:
  - AF ablation = intervention selection
  - inherited cardiomyopathy = surveillance intensity
  - post-MI care = follow-up and treatment optimization

### 2. Make the patient benefit concrete

Avoid generic claims like "improve outcomes" and instead say things like:

- reduce unnecessary ablation and low-yield surveillance
- identify patients with the greatest predicted benefit from invasive or intensive care
- safely de-escalate follow-up where high negative predictive value is achieved
- support earlier escalation when latent trajectories worsen
- improve patient-facing explanations and follow-up planning without replacing clinicians

### 3. Put implementation into the science, not after it

BHF is unlikely to love a proposal that says regulation and HTA will be considered later.

Include explicit work on:

- NICE ESF-aligned evidence generation
- MHRA/FDA-compatible lifecycle monitoring
- health economics and service redesign
- subgroup fairness and equity analysis
- human factors and workflow integration
- prospective or shadow-mode evaluation pathways

### 4. Use AI-ECG as an enabling layer, not the whole pitch

The deeper review strengthens AI-ECG as part of the story, but not as the centre of gravity.

Best use in the application:

- as a scalable, low-cost phenotyping and screening modality
- as a trigger for richer imaging, genetic, or EHR review
- as a way to make longitudinal monitoring more NHS-realistic

Avoid letting the proposal drift into "we also do AI-ECG" as a separate mini-project.

### 5. Keep LLMs strictly subordinate

The current literature supports LLMs mainly for:

- patient explanation
- consent-support drafting
- MDT summarization
- procedure-prep information
- documentation support

It does *not* support making LLM-guided procedures or autonomous perioperative decisions a major scientific claim.

If included, LLMs should sit inside an implementation and communication work package, not at the core of the proposal.

### 6. Make the team architecture reviewer-friendly

The team should visibly include:

- causal inference and treatment-effect estimation expertise
- longitudinal and multimodal ML expertise
- AF electrophysiology expertise
- inherited cardiomyopathy and cardiovascular genetics expertise
- acute coronary syndrome, rehabilitation, and secondary prevention expertise
- NHS implementation and health economics expertise
- regulatory and device-governance expertise
- patient and public contributors with real authority
- ideally one SME or platform partner with deployment experience

### 7. Use milestone language

The year-1 review means reviewers will want credible early outputs.

Suggested milestone logic:

- Year 1: data harmonization, governance, target-trial definitions, baseline benchmarks, patient/public co-design
- Year 2: retrospective multimodal models, AI-ECG integration studies, subgroup auditing
- Year 3: temporal updating, decision-policy modelling, LLM-supported communication prototypes in shadow mode
- Year 4: external validation, health-economic modelling, workflow pilots, shadow deployment
- Year 5: prospective evaluation package and scale-up roadmap

## Likely weak points to fix before submission

### Weak point 1: observational treatment-effect estimation can sound causal without enough defence
Add:

- explicit target-trial emulation language
- treatment-policy estimands defined prospectively
- negative controls and sensitivity analyses
- external validation across institutions
- prespecified subgroup transportability checks

### Weak point 2: multimodal data access may sound aspirational
Add:

- named datasets and sites
- what data already exist versus what must be prospectively collected
- fallback plan if wearables are sparse
- a minimum viable model if the richest multimodal stack is delayed

### Weak point 3: post-MI theme may feel less differentiated than the other two
Strengthen with:

- a sharper decision target, for example follow-up intensity, rehab allocation, medication intensification, or imaging review escalation
- explicit time-updated prediction windows
- service-linked endpoints, not just mortality or MACE

### Weak point 4: proposal could drift into generic AI optimism
Counter this explicitly:

- the aim is not autonomy
- clinician oversight is required
- fairness, calibration, and interpretability are primary outputs
- success includes safe non-intervention, not just more intervention
- LLM outputs will be verified and never treated as self-validating evidence

## Useful phrases to recycle in the proposal

- *step-change in impact or ambition*
- *from discovery to clinical practice*
- *large integrated programme*
- *clear path to impact*
- *meaningful involvement of people with lived experience*
- *robust management and governance*
- *responsible AI*
- *NHS-ready evidence generation*
- *clinician-supervised decision support*

## Recommended punchy positioning sentence

*We will build and validate a generalizable, NHS-ready AI framework for individualized cardiovascular decisions, estimating who benefits from intervention, who requires closer surveillance, and who can be safely spared unnecessary follow-up, while using scalable signals such as ECG to widen practical reach.*

## Recommended reviewer-facing contrast sentence

*This is not a proposal for another cardiovascular risk score, a standalone AI-ECG product, or an autonomous LLM assistant. It is a programme to move from static risk estimation to dynamic, individualized decisions about treatment, surveillance, and follow-up.*
