# Search log: USA congenital heart disease statistics

## Scope lock for the final dossier draft

- Work restricted to `vespa_library`.
- Final evidence is limited to PMIDs returned in the original PubMed search-result sets captured on 2026-04-19.
- A later Codex-assisted pass in a temporary worktree surfaced additional potentially useful CHD papers, but any PMID outside the approved search-result sets was excluded from the final draft.
- This log records both the original search sets and the final source-constrained retention decisions.

## Original PubMed search runs

### Search 1: prevalence / incidence / population
- *Database:* PubMed
- *Search name:* CHD USA prevalence
- *Date run:* 2026-04-19
- *Searcher:* OpenClaw assistant
- *Exact query:* `((congenital heart disease[Title/Abstract]) OR (congenital heart defect*[Title/Abstract])) AND (United States[Title/Abstract] OR USA[Title/Abstract]) AND (prevalence OR incidence OR population)`
- *PMIDs returned for first pass:* 36695182, 38264914, 39866113, 33501848, 31992061, 35078371, 41562125, 31580536
- *Final use:* retained PMID 33501848 and 31580536 for quantitative extraction; newer AHA updates remained context sources only.

### Search 2: mortality / deaths / survival
- *Database:* PubMed
- *Search name:* CHD USA mortality and survival
- *Date run:* 2026-04-19
- *Searcher:* OpenClaw assistant
- *Exact query:* `((congenital heart disease[Title/Abstract]) OR (congenital heart defect*[Title/Abstract])) AND (United States[Title/Abstract] OR USA[Title/Abstract]) AND (mortality OR deaths OR survival)`
- *PMIDs returned for first pass:* 33501848, 31992061, 25638345, 37704344, 27390667, 35641458, 39947807, 29463390
- *Final use:* retained PMID 33501848 for a national mortality rate; retained PMID 32123122 and 30976885 from the surgery-related searches for survival-adjacent operative outcome metrics.

### Search 3: surgery / operations / procedures
- *Database:* PubMed
- *Search name:* CHD USA surgery volume
- *Date run:* 2026-04-19
- *Searcher:* OpenClaw assistant
- *Exact query:* `((congenital heart disease[Title/Abstract]) OR (congenital heart defect*[Title/Abstract])) AND (United States[Title/Abstract] OR USA[Title/Abstract]) AND (surgery OR operations OR procedure OR intervention)`
- *PMIDs returned for first pass:* 25638345, 27390667, 39947807, 29463390, 26876122, 28617685, 32123122, 32622484
- *Final use:* retained PMID 28617685 for adult burden context and PMID 32123122 for aggregate operative mortality; direct national surgery volume ultimately came from allowed AHA source PMID 33501848.

### Search 4: adult congenital heart disease burden
- *Database:* PubMed
- *Search name:* Adult CHD USA burden
- *Date run:* 2026-04-19
- *Searcher:* OpenClaw assistant
- *Exact query:* `adult congenital heart disease United States prevalence mortality surgery`
- *PMIDs returned for first pass:* 20579534, 35491368, 30032387, 29472380, 36580104, 38018491, 14999190, 30976885
- *Final use:* retained PMID 35491368, 36580104, 38018491, 14999190, and 30976885.

## Final retained PMIDs for the compliant dossier draft

- **PMID 33501848** — AHA 2021 statistics update; used for all-age prevalence, adult prevalence ratio, age-adjusted mortality rate, national congenital heart surgery volume, and most common primary procedure.
- **PMID 31580536** — national birth prevalence for 12 critical CHD defects combined.
- **PMID 14999190** — historical survivor-count estimates with and without treatment, useful for survival framing.
- **PMID 28617685** — adult CHD burden review citing more than 1 million affected adults in the United States.
- **PMID 35491368** — updated adult burden review citing more than 1.4 million US adults living with congenital heart defects.
- **PMID 30976885** — ACHD surgery admissions, complication burden, and in-hospital mortality during 2005 to 2009.
- **PMID 32123122** — aggregate pediatric congenital heart surgery operative mortality of approximately 3%.
- **PMID 36580104** — all-payer ACHD surgery cohort size during 2005 to 2014.
- **PMID 38018491** — ACHD heart-failure admission burden and excess mortality risk.

## Quantitative facts extracted into the final dossier

### Cases and prevalence
- `PMID 33501848`: estimated prevalence of congenital cardiovascular defects in all age groups in the United States was **2.4 million** in 2010.
- `PMID 33501848`: **1 in 150 adults** in the United States is expected to have some form of congenital heart defect.
- `PMID 35491368`: **>1.4 million adults** in the United States are estimated to be living with a congenital heart defect.
- `PMID 31580536`: adjusted national birth prevalence for the **12 critical CHD defects combined was 19.93 per 10,000 live births**.

### Mortality and survival
- `PMID 33501848`: in 2018, the age-adjusted death rate attributable to congenital cardiovascular defects in the United States was **0.9 per 100,000**.
- `PMID 32123122`: current aggregate operative mortality for congenital heart surgery in children was **approximately 3%**.
- `PMID 30976885`: mortality during ACHD surgery admissions was **4.6% with a complication versus 0.9% without**.
- `PMID 14999190`: treated-survivor projections were **750,000 simple**, **400,000 moderate**, and **180,000 complex** lesions, compared with **400,000**, **220,000**, and **30,000** without treatment.

### Surgery volume and procedure profile
- `PMID 33501848`: **123,777 congenital heart surgeries** were performed from January 2015 to December 2018 in the Society of Thoracic Surgeons Congenital Heart Surgery Database.
- `PMID 33501848`: **delayed sternal closure** was the most common primary procedure.
- `PMID 30976885`: **16,841 ACHD surgery admissions** were identified in ages 18 to 49 during 2005 to 2009.
- `PMID 36580104`: **174,370 patients** underwent ACHD surgery in a US all-payer database during 2005 to 2014.

## Explicit exclusions after validation

The following PMIDs were surfaced during the Codex-assisted drafting pass but were **not** merged into the final dossier because they were outside the user-approved PubMed result sets:

- 27382105
- 24222433
- 21098447
- 40698377
- 29793633
- 31272703
- 38522772
- 21911232
- 23804929

## Remaining caveats

- The approved PMID set supports a solid first-pass dossier for prevalence, mortality, surgery burden, and operative outcomes.
- It is weaker for a single modern national long-term survival rate by lesion class. The final report therefore uses transparent operative-mortality and survivor-count proxies rather than claiming a stronger long-term survival estimate than the approved source set supports.
