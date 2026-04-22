# Reviewer passes, ventricular arrhythmias R01 aims page

## Current baseline
The current Overleaf draft is a solid first-pass Specific Aims page, but it still reads more like a strong technical concept note than a mature R01 aims page that has been pressure-tested by multiple reviewer mindsets.

## Pass 1, clinical reviewer

### What this reviewer will like
- The disease problem is clinically important.
- The proposal connects to real decisions: VT ablation, pacing, and Brugada evaluation.
- The page is clearly translational rather than purely computational.

### Likely concerns
- The opening paragraph still starts a little too method-first for a busy electrophysiology reviewer.
- The patient benefit should be sharper and earlier.
- The three clinical settings may feel broad unless staged more explicitly.

### Revision targets
- Put clinical pain points and patient impact even more upfront.
- Clarify what is currently not knowable from ECG, imaging, and EP studies alone.
- Emphasize that the platform is intended to improve decision-making, not just produce prettier maps.

### Clinical-pass edits to make
- Strengthen opening line around sudden death, HF progression, recurrent VT, failed or repeated procedures.
- Add one sentence that current assessments do not explain mechanism at the individual-patient level.
- Tighten Aim 3 endpoints around localization, prediction of pacing response, and clinically meaningful subgrouping.

## Pass 2, technical reviewer

### What this reviewer will like
- Forward-calibrated mechanistic modeling is a serious conceptual advance over simple inverse reconstruction.
- The pipeline from automation to calibration to prospective testing is logical.

### Likely concerns
- The distinction between inverse ECGi and forward-calibrated inference should be even crisper.
- Aim 2 risks sounding broad unless the inferable parameter classes are prioritized.
- Reviewers will worry about identifiability, uncertainty, and computational tractability.

### Revision targets
- Explicitly state why alternative internal states can generate similar body-surface signals and why that matters.
- Use fewer generic words like "mechanistic" unless paired with concrete parameter classes.
- Make uncertainty-aware inference a visible strength, not a side note.

### Technical-pass edits to make
- Add a sentence on ill-posedness and non-uniqueness of inverse reconstruction.
- Narrow Aim 2 wording to a tractable set of inferable quantities: activation sequence, initiation site, conduction slowing, scar-associated substrate, repolarization heterogeneity.
- State that staged calibration and emulation are used to preserve feasibility.

## Pass 3, NIH grantsmanship reviewer

### What this reviewer will like
- The proposal has a clear overall objective, central hypothesis, and three aims.
- The final paragraph includes significance, innovation, and impact.

### Likely concerns
- The central hypothesis can be made more testable by tying it more explicitly to Aim 3 outcomes.
- The rationale paragraph is good, but it can be more forceful about why now is the right time.
- Expected outcomes should be a little more concrete.

### Revision targets
- Make the hypothesis more visibly testable.
- Recast the final paragraph so significance and innovation are more reviewer-facing.
- Use deliverable language for each aim.

### Grantsmanship-pass edits to make
- Rephrase the hypothesis to include improved localization, therapy-response prediction, and mechanistic classification.
- In each aim, end with a cleaner deliverable sentence.
- Add a more memorable closing impact sentence.

## Pass 4, feasibility and risk reviewer

### What this reviewer will like
- The project is ambitious but coherent.
- The preliminary infrastructure suggests this is not starting from zero.

### Likely concerns
- VT, pacing, and Brugada together could feel like too much for one R01.
- Prospective evaluation across three settings may raise timeline concerns.
- Reviewers may worry about data heterogeneity, computational speed, and calibration failure modes.

### Revision targets
- Show that the project is one platform tested across three use cases, not three unrelated projects.
- Make staged evaluation explicit.
- Reduce any sentence that implies all components will be solved at once.

### Feasibility-pass edits to make
- Use language like "three complementary testbeds for one common platform".
- Add wording that the retrospective work de-risks the prospective deployment.
- Avoid promising direct clinical deployment in the R01 period.

## Pass 5, anti-AI-writing reviewer

### What this reviewer will flag
- Generic transitional phrasing.
- Repetitive sentence rhythm.
- Too many abstract nouns without concrete anchors.
- Standard LLM phrasing such as "major unmet need" or "lay the groundwork" if overused.

### Revision targets
- Vary sentence structure.
- Replace generic emphasis with sharper domain-specific claims.
- Keep the writing sounding like a real grant from a PI who knows the clinical and technical terrain.

### Anti-AI edits to make
- Cut repeated uses of "mechanistic", "patient-specific", and "non-invasive" unless each is doing work.
- Replace stock phrases with more exact language.
- Remove any sentence that sounds like a generic innovation paragraph rather than electrophysiology-specific argument.

## Pass 6, final compression and one-page polish

### Final checklist
- Must fit comfortably on a one-page Specific Aims layout.
- Every sentence should either increase reviewer confidence or carry scientific content.
- Aim titles should be parallel and easy to skim.
- The first paragraph and last paragraph should be the strongest prose on the page.

### Final-pass edits to make
- Compress long sentences in Aim 2 and Aim 3.
- Keep only the strongest preliminary-data sentence.
- Ensure opening burden statement and final impact statement are memorable.

## Pass 7, reference existence reviewer

### Reviewer task
- Confirm that every proposed PMID resolves to a real, online PubMed record.
- Flag any missing, outdated, or off-topic citations.

### Status
- Completed in `pmid_verification.md`.
- All current candidate PMIDs used in the map resolve online through PubMed.

## Pass 8, reference-to-claim mapping reviewer

### Reviewer task
- Double and triple check that each PMID actually supports the sentence it is paired with.
- Prevent citation drift, where a paper is real but does not actually support the exact point made.

### Status
- Completed in `pmid_verification.md`.
- Strong versus moderate mapping strength is explicitly documented.

## Immediate next writing action
The next revision should do three things at once:
1. sharpen the opening clinically,
2. make the inverse-versus-forward distinction more technical and more explicit,
3. trim generic phrasing so the page sounds less templated and more reviewer-proof.
