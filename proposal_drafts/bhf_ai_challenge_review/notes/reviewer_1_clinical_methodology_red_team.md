# Reviewer 1: Clinical and methodology red team

Persona: senior cardiovascular trialist with zero patience for AI hype.

## Default attitude

"If you cannot show me the exact clinical decision, the comparator, the bias control, and the implementation consequence, I am not funding this."

## Core attack questions

1. What exact decision is each model supposed to change?
   - AF: offer ablation, timing of ablation, or follow-up intensity after ablation?
   - Cardiomyopathy: screening interval, escalation to CMR/genetics, or discharge from close surveillance?
   - Post-MI: rehab intensity, clinic frequency, medication optimization, imaging, or all of the above?

2. Are you estimating benefit or merely predicting events?
   - Show estimand definitions.
   - Show treatment-policy question.
   - Show how confounding by indication will be handled.

3. What is the baseline comparator?
   - guideline-based care
   - clinician judgement
   - standard risk score
   - simple parsimonious model

4. Why these three domains together?
   - What common methodological engine unifies them?
   - Why is a single programme better than three focused grants?

5. Where is the prospective or external validation plan?
   - internal cross-validation is not enough
   - site shift and temporal shift must be tested

6. What is the failure mode?
   - what happens if the model is wrong
   - what safety override exists
   - how will low-confidence predictions be handled

## Non-negotiable fixes before final submission

- Define 1 primary decision target per workstream.
- State causal assumptions and sensitivity analyses plainly.
- Include at least one external validation cohort per domain.
- Include a policy baseline comparator, not only ML-vs-ML benchmarks.
- State exactly how NPV thresholds will be chosen and clinically justified.

## Evidence checks this reviewer will demand

- CABANA average effect and subgroup heterogeneity must be cited accurately. PMIDs 30874766 and 41213867.
- DECAAF recurrence gradient must not be exaggerated. PMID 24496537.
- DCM family-screening yield and HCM low-yield follow-up subgroup must be numerically correct. PMIDs 37225358 and 39365224.
- Post-MI workstream needs a stronger, concrete endpoint and intervention logic.

## What would impress this reviewer

- explicit target-trial emulation language
- prespecified subgroup and fairness analysis
- clinically interpretable thresholds
- external validation plus shadow-mode deployment
- a serious plan for negative or null results
