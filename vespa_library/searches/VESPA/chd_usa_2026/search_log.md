# Search log: USA congenital heart disease statistics

## Search record template

- *Database:*
- *Search name:*
- *Date run:*
- *Searcher:*
- *Exact query:*
- *Filters applied:*
- *Hits returned:*
- *Screening decision summary:*
- *Inclusion notes:*
- *Exclusion notes:*
- *Export file(s):*
- *Next action:*

## Planned search blocks

1. Incidence and prevalence in the USA
2. Mortality and cause-specific death statistics
3. Survival rates by age group / lesion severity
4. Surgical volume and procedure classes
5. Adult congenital heart disease burden
6. Recent national registry and CDC summaries

## Initial PubMed search runs

### Search 1: prevalence / incidence / population
- *Database:* PubMed
- *Search name:* CHD USA prevalence
- *Date run:* 2026-04-19
- *Searcher:* OpenClaw assistant
- *Exact query:* `((congenital heart disease[Title/Abstract]) OR (congenital heart defect*[Title/Abstract])) AND (United States[Title/Abstract] OR USA[Title/Abstract]) AND (prevalence OR incidence OR population)`
- *Filters applied:* none recorded
- *PMIDs returned for first pass:* 36695182, 38264914, 39866113, 33501848, 31992061, 35078371, 41562125, 31580536
- *Screening decision summary:* prioritize AHA annual statistics updates and national population-based defect estimates
- *Inclusion notes:* useful for prevalence, incidence, and national burden framing
- *Exclusion notes:* some hits may be broad cardiovascular statistics updates rather than CHD-focused primary sources
- *Export file(s):* manual PMID capture only so far
- *Next action:* inspect AHA tables and the birth-defects population estimate paper for explicit CHD counts

### Search 2: mortality / deaths / survival
- *Database:* PubMed
- *Search name:* CHD USA mortality and survival
- *Date run:* 2026-04-19
- *Searcher:* OpenClaw assistant
- *Exact query:* `((congenital heart disease[Title/Abstract]) OR (congenital heart defect*[Title/Abstract])) AND (United States[Title/Abstract] OR USA[Title/Abstract]) AND (mortality OR deaths OR survival)`
- *Filters applied:* none recorded
- *PMIDs returned for first pass:* 33501848, 31992061, 25638345, 37704344, 27390667, 35641458, 39947807, 29463390
- *Screening decision summary:* likely mixed yield, with AHA reports most promising and several screening / obstetric papers likely off-target for national mortality counts
- *Inclusion notes:* retain AHA updates and adult CHD mortality-focused papers for closer review
- *Exclusion notes:* probable noise from newborn screening and obstetric management papers if they do not provide national CHD death data
- *Export file(s):* manual PMID capture only so far
- *Next action:* identify explicit mortality and survival figures with PMIDs and quotes

### Search 3: surgery / operations / procedures
- *Database:* PubMed
- *Search name:* CHD USA surgery volume
- *Date run:* 2026-04-19
- *Searcher:* OpenClaw assistant
- *Exact query:* `((congenital heart disease[Title/Abstract]) OR (congenital heart defect*[Title/Abstract])) AND (United States[Title/Abstract] OR USA[Title/Abstract]) AND (surgery OR operations OR procedure OR intervention)`
- *Filters applied:* none recorded
- *PMIDs returned for first pass:* 25638345, 27390667, 39947807, 29463390, 26876122, 28617685, 32123122, 32622484
- *Screening decision summary:* likely contextual rather than directly quantitative; surgery-specific utilization papers need prioritization over screening or workforce reviews
- *Inclusion notes:* keep adult CHD magnitude/problem papers and congenital heart surgery morbidity/quality pieces for procedure framing
- *Exclusion notes:* likely drop transplant or screening papers unless they provide concrete CHD surgery counts or types
- *Export file(s):* manual PMID capture only so far
- *Next action:* search specifically for STS / national registry procedure counts and surgery class breakdowns

### Search 4: adult congenital heart disease burden
- *Database:* PubMed
- *Search name:* Adult CHD USA burden
- *Date run:* 2026-04-19
- *Searcher:* OpenClaw assistant
- *Exact query:* `adult congenital heart disease United States prevalence mortality surgery`
- *Filters applied:* none recorded
- *PMIDs returned for first pass:* 20579534, 35491368, 30032387, 29472380, 36580104, 38018491, 14999190, 30976885
- *Screening decision summary:* several useful adult CHD context papers found, mixed with obvious off-target records
- *Inclusion notes:* retain adult CHD mortality, surgery morbidity, and burden papers for secondary evidence extraction
- *Exclusion notes:* drop clearly unrelated cardiovascular topics such as spontaneous coronary artery dissection
- *Export file(s):* manual PMID capture only so far
- *Next action:* separate adult CHD outcome papers from off-target noise and pull direct USA figures where available
