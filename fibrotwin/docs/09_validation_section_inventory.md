# Validation Page Section Inventory

## Section-by-section documentation

### 1) Model QA
- **Contains:** test outcomes, verification scope summary, metric dictionary.
- **Presentation:** status lists + definition table.
- **Purpose:** establish metric meanings and baseline trust in numerics.

### 2) Core validation outcomes
- **Contains:** validation card, infarct panel, portfolio table, scenario matrix table + explorer, UQ summary, drug validation, matrix interpretation.
- **Presentation:** summary tiles + structured tables + figures.
- **Purpose:** show biological/mechanistic outcomes and intervention trends.

### 3) Method QA
- **Contains:** numerical verification cards, calibration cards, emulation/history matching, parameter audit.
- **Presentation:** clickable card system and detailed subpages.
- **Purpose:** show computational and calibration robustness.

### 4) Coverage and evidence
- **Contains:** uniqueness audit, mechanism coverage matrix, systematic literature-linked catalog, publication figures, per-test card gallery, failure-group summary.
- **Presentation:** evidence tables + card gallery.
- **Purpose:** demonstrate breadth/depth and traceability to literature.

## Similarities across sections
- Card-based visual framing.
- Table-centric summaries for comparability.
- PASS/FAIL style cues where relevant.
- Links to drill-down detail pages.

## Differences across sections
- Model QA focuses on definitions and immediate checks.
- Core outcomes focuses on scenario behavior and interventions.
- Method QA focuses on algorithmic/numerical/calibration credibility.
- Coverage/evidence focuses on literature mapping and test catalog breadth.

## Unified structure used for all sections
Each section now follows:
1. **Section header + purpose line**
2. **Summary tiles** (where available)
3. **Primary structured table**
4. **Optional figure(s)/interactive element**
5. **Links to detail cards/pages**

This common structure is now used across validation page sections and enforced by shared styling and build templates.
