# Validation Page Unification Plan

## Problems observed
- Mixed old/new sections (some markdown dumps, some card-native sections).
- Repeated content blocks and duplicated interpretations.
- Scenario names are machine-like and hard to read.
- Some PMID test cards appear to share near-identical outcome style.

## Target structure (single coherent section)
1. **Pipeline overview** (what readers should read first).
2. **Model QA summary** (tests passed, verification scope).
3. **Metric dictionary** (definitions + units).
4. **Core validation outcomes**
   - validation portfolio table,
   - scenario matrix (human-readable labels),
   - UQ table.
5. **Intervention validation**
   - drug card,
   - infarct region panel.
6. **Method QA cards**
   - numerical verification cards,
   - calibration cards,
   - emulation/history matching cards.
7. **Coverage & evidence**
   - uniqueness audit,
   - coverage matrix,
   - literature-linked catalog,
   - per-test card gallery.

## Style contract (applies to all future edits)
- Use one card system and one badge system (`PASS/FAIL`).
- Every detail page uses the same 5-block layout:
  1) summary, 2) simulation setup, 3) common visualization, 4) interpretation, 5) back link.
- No raw markdown tables in rendered page content.
- Scenario names must be human-readable labels.

## Quantitative upgrade for similar tests (e.g., T002/T003)
When tests have similar qualitative outcomes, differentiate using quantitative descriptors:
- endpoint delta (% change vs control),
- normalized error to target band center,
- rank/score against study-specific expected range,
- confidence tag (screening vs extracted quantitative evidence).

## Immediate actions
- [x] Human-readable scenario labels on validation tables.
- [x] Remove repeated legacy appendices from validation landing page.
- [ ] Add per-test quantitative comparator row (delta, normalized residual) for all T-cards.
- [ ] Add category-wise distribution plots so similar tests are visibly separable by quantitative score.
