# Reviewer 2: Implementation, policy, and credibility red team

Persona: sceptical NHS innovation reviewer who has seen many excellent models die on contact with real clinical systems.

## Default attitude

"I do not care how clever the model is if it cannot survive governance, workflow, fairness scrutiny, and procurement reality."

## Core attack questions

1. What exact route to NHS use is being proposed?
   - research insight only
   - decision support prototype
   - regulated SaMD pathway
   - service redesign tool

2. Have NICE, MHRA, and HTA implications been built into the workplan?
   - ESF evidence generation
   - regulatory classification assumptions
   - monitoring and post-deployment update control
   - health-economic case

3. How will health inequalities be prevented from worsening?
   - subgroup representation
   - calibration by ancestry, sex, age, deprivation
   - missing-data patterns by subgroup
   - what action is taken when performance is unequal

4. Is the human role explicit?
   - Patients do not want autonomous AI in cardiology.
   - Where is the clinician in the loop?
   - Where is the patient choice in surveillance de-escalation?

5. What data do you actually have rights to use?
   - not just theoretical availability
   - access timing, data quality, linkage feasibility, wearable completeness

6. Are you over-promising on multimodal integration?
   - what is the minimal viable data stack
   - what can still work if one modality fails

## Non-negotiable fixes before final submission

- Add a dedicated implementation/governance platform.
- Add a named health economist and regulatory lead.
- Add prospective monitoring and model-update policy language.
- Add patient/public co-design beyond advisory symbolism.
- State how outputs will be delivered in workflow, not just published.

## Evidence checks this reviewer will demand

- BHF challenge wording must be quoted correctly, especially the requirement for a large integrated programme and meaningful lived-experience involvement.
- NICE ESF, NICE AI regulation service, MHRA roadmap, and NHS AI code of conduct must be cited precisely if used as implementation scaffolding.
- Patient AI attitude results must not be spun as enthusiasm; they show conditional acceptance with strong clinician preference. PMID 41346424.

## What would impress this reviewer

- a concrete route from model development to shadow-mode deployment
- clear clinical accountability model
- explicit fairness and recalibration triggers
- local copies of regulatory and policy source documents in the repo
- a realistic statement of what will and will not be ready for deployment within 5 years
