---
name: bibtex-validator
description: Validate BibTeX files and auto-generate correct \cite{} commands for LaTeX documents. Use when: (1) checking if BibTeX keys match \cite{} commands in documents, (2) extracting all BibTeX entry keys, (3) finding undefined citations, (4) auto-correcting citation mismatches, (5) generating complete reference sections from BibTeX metadata.
---

# BibTeX Validator & Citation Checker

Ensure your LaTeX documents cite only entries that exist in your BibTeX file, with exact key matching.

## Quick Start

```bash
# Check if all citations in document match BibTeX file
bibtex-validator check document.tex references.bib

# Extract all BibTeX keys
bibtex-validator list references.bib

# Find undefined citations
bibtex-validator missing document.tex references.bib

# Auto-correct citations (generates corrected document)
bibtex-validator fix document.tex references.bib output.tex
```

## What This Skill Does

### 1. Extract BibTeX Keys
Reads `references.bib` and lists all available citation keys:

```
Found 33 BibTeX entries:
- zhou2025evlp
- inheart2024fda
- sophia2024oncology
- ebenbuild2025twinhale
...
```

### 2. Extract Citations from LaTeX
Finds all `\cite{...}` commands in document and lists them:

```
Found 19 citations in document.tex:
- \cite{zhou2025evlp}
- \cite{inheart2024fda}
- \cite{ebenbuild2025twinhale}
...
```

### 3. Check for Mismatches
Compares BibTeX keys against document citations:

```
UNDEFINED CITATIONS (in document but NOT in .bib):
- Missing: 'zhou2025evlpXX' (should be 'zhou2025evlp')
- Missing: 'inheartt2024fda' (should be 'inheart2024fda')

UNUSED ENTRIES (in .bib but NOT cited):
- Unused: 'fibresolve2023' (defined but never cited)
```

### 4. Auto-Fix Citations (Optional)
Generates a corrected document by matching citations to BibTeX keys:

```
Processing document.tex...
  Line 5: \cite{zhou2025evlpXX} → \cite{zhou2025evlp} ✓
  Line 10: \cite{inheartt2024fda} → \cite{inheart2024fda} ✓
Writing corrected document to output.tex
```

### 5. Generate Citation Commands
Creates a list of all correct `\cite{}` commands ready to copy-paste:

```
All valid citations (copy-paste ready):
\cite{zhou2025evlp}
\cite{inheart2024fda}
\cite{sophia2024oncology}
\cite{ebenbuild2025twinhale}
...
```

## Usage Examples

### Example 1: Validate a Document

```bash
bibtex-validator check document.tex references.bib
```

**Output:**
```
BibTeX file: references.bib
LaTeX document: document.tex

BibTeX entries: 33
Citations in document: 19

VALIDATION RESULT: ✓ ALL CITATIONS VALID
- All 19 citations found in BibTeX file
- No undefined references
- No unused entries in bibliography
```

### Example 2: Find Undefined Citations

```bash
bibtex-validator missing document.tex references.bib
```

**Output:**
```
UNDEFINED CITATIONS:
Line 5:  \cite{zhou2025evlpXX}
Line 10: \cite{inheartt2024fda}
Line 15: \cite{unknownkey}

SUGGESTIONS:
  'zhou2025evlpXX' → Did you mean 'zhou2025evlp'?
  'inheartt2024fda' → Did you mean 'inheart2024fda'?
  'unknownkey' → No close match found
```

### Example 3: Auto-Fix Document

```bash
bibtex-validator fix document.tex references.bib document_fixed.tex
```

**Output:**
```
Fixed 3 citation mismatches:
  Line 5:  zhou2025evlpXX → zhou2025evlp
  Line 10: inheartt2024fda → inheart2024fda
  Line 15: unknownkey → [REMOVED - not in BibTeX]

Corrected document written to: document_fixed.tex
Backup: document.tex.backup
```

### Example 4: Generate Valid Citation List

```bash
bibtex-validator list references.bib --format latex
```

**Output:**
```
% All valid BibTeX keys (ready for LaTeX)

\cite{zhou2025evlp}
\cite{inheart2024fda}
\cite{sophia2024oncology}
\cite{ebenbuild2025twinhale}
\cite{genentech2024pbpk}
\cite{fibresolve2023}
\cite{multimodal2024uip}
\cite{sipro2024aid}
...
```

## Key Features

### Typo Detection
Automatically detects common BibTeX key typos:
- Extra/missing characters: `zhou2025evlpXX` → suggest `zhou2025evlp`
- Capitalization: `Inheart2024FDA` → suggest `inheart2024fda`
- Transposition: `inheartt2024fda` → suggest `inheart2024fda`

### Case Sensitivity Handling
BibTeX keys are case-sensitive. The validator:
- Warns if keys differ only by case
- Suggests lowercase convention (standard in LaTeX)
- Auto-corrects if `--fix` flag used

### Citation Extraction
Handles all citation formats:
- `\cite{key}` — single citation
- `\cite{key1,key2,key3}` — multiple citations
- `\cite{key1} and \cite{key2}` — separate citations
- `\citet{key}` and `\citep{key}` — natbib variants

### Batch Processing
Process entire directories:

```bash
bibtex-validator check *.tex references.bib --recursive
```

## Integration with Workflow

### Before Committing to Overleaf

```bash
# Check document before push
bibtex-validator check lung_digital_twins_review.tex references.bib

# If errors found, auto-fix
bibtex-validator fix lung_digital_twins_review.tex references.bib lung_digital_twins_review.tex

# Verify fix worked
bibtex-validator check lung_digital_twins_review.tex references.bib
```

### During Document Development

```bash
# Quick check after editing
bibtex-validator check document.tex references.bib --quiet

# Only show errors, not warnings
bibtex-validator check document.tex references.bib --errors-only
```

### Generate Bibliography Report

```bash
bibtex-validator report references.bib
```

**Output:**
```
BibTeX Bibliography Report
========================

Total entries: 33
Cited in documents: 19
Unused: 14

Entry Types:
  @article: 25
  @preprint: 5
  @techreport: 2
  @misc: 1

Key Format:
  lowercase: 28
  MixedCase: 4
  UPPERCASE: 1

Recommendation: Standardize to lowercase keys (28/33 already follow this)
```

## When to Use This Skill

✓ **Before compiling LaTeX in Overleaf**
✓ **After editing document citations**
✓ **When adding new BibTeX entries**
✓ **When merging BibTeX files**
✓ **Before pushing to version control**
✓ **When fixing "undefined citation" warnings**

✗ NOT needed: For simple documents with 1-2 citations
✗ NOT needed: If you never modify citations

## Common Errors It Catches

| Error | Detection | Suggestion |
|-------|-----------|-----------|
| `\cite{zhou2025evlp}` but key is `Zhou2025EVLP` | Case mismatch | Use lowercase: `zhou2025evlp` |
| `\cite{fibresolve2023}` but not in .bib | Undefined citation | Check spelling or add to .bib |
| Typo: `\cite{fibresolv2023}` (missing 'e') | Fuzzy match | Did you mean `fibresolve2023`? |
| Extra citation: `\cite{unused2024}` | Unused entry | Remove from document or add to .bib |
| Multiple citations: `\cite{a,b,c}` | Checks all keys | Validates all three entries |

## Tips for BibTeX Maintenance

1. **Use consistent key format**: `author+year+firstword`
   - Good: `zhou2025evlp`, `fibresolve2023`, `inheart2024fda`
   - Avoid: `Zhou_2025_EVLP`, `Fibresolve-IPF-2023`

2. **Document citation keys in a reference sheet**:
   ```
   # Digital Twins Review - Citation Keys
   - Toronto EVLP: zhou2025evlp
   - inHEART FDA: inheart2024fda
   - Fibresolve: fibresolve2023
   ```

3. **Run validator before each Overleaf push**

4. **Keep BibTeX file organized** by entry type or topic:
   ```
   % CLINICAL TWINS
   @article{zhou2025evlp,...}
   @article{inheart2024fda,...}
   
   % DIAGNOSTIC AI
   @article{fibresolve2023,...}
   @article{sipro2024aid,...}
   ```

## Requirements

- LaTeX document with `\cite{}` commands
- BibTeX file (.bib) with `@article{key,...}` entries
- Python 3.6+ (for fuzzy matching of typos)

## Output

Generates:
- **Validation report** (console)
- **Corrected LaTeX document** (if `--fix` used)
- **Citation list** (if `--format latex` used)
- **Bibliography report** (if `report` subcommand used)

No modifications to original files unless `--fix` flag is used (creates .backup).
