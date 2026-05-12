#!/usr/bin/env python3
"""
BibTeX Validator - Check LaTeX citations against BibTeX entries
Usage: python3 bibtex_validator.py check document.tex references.bib
"""

import re
import sys
from pathlib import Path
from difflib import SequenceMatcher

def extract_bibtex_keys(bib_file):
    """Extract all BibTeX keys from .bib file"""
    keys = {}
    with open(bib_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find all @type{key, ... } patterns
    pattern = r'@\w+\{([^,]+),'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        key = match.group(1).strip()
        keys[key] = True
    
    return keys

def extract_citations(tex_file):
    """Extract all \\cite{...} commands from LaTeX file"""
    citations = []
    with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find all \cite{...} patterns
    pattern = r'\\cite\{([^}]+)\}'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        # Handle multiple citations like \cite{a,b,c}
        keys_str = match.group(1)
        keys = [k.strip() for k in keys_str.split(',')]
        for key in keys:
            citations.append((key, match.start()))
    
    return citations

def find_closest_match(typo, valid_keys, threshold=0.8):
    """Find closest BibTeX key using fuzzy matching"""
    best_match = None
    best_ratio = 0
    
    for key in valid_keys:
        ratio = SequenceMatcher(None, typo.lower(), key.lower()).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = key
    
    return best_match if best_ratio >= threshold else None

def validate(tex_file, bib_file, verbose=True):
    """Validate LaTeX citations against BibTeX"""
    bibtex_keys = extract_bibtex_keys(bib_file)
    citations = extract_citations(tex_file)
    
    undefined = []
    valid = []
    
    for cite_key, pos in citations:
        if cite_key in bibtex_keys:
            valid.append(cite_key)
        else:
            undefined.append((cite_key, find_closest_match(cite_key, bibtex_keys)))
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"BibTeX Validator Report")
        print(f"{'='*60}")
        print(f"LaTeX file: {tex_file}")
        print(f"BibTeX file: {bib_file}")
        print(f"\nBibTeX entries: {len(bibtex_keys)}")
        print(f"Citations found: {len(citations)}")
        print(f"Valid citations: {len(valid)}")
        print(f"Undefined citations: {len(undefined)}")
        
        if undefined:
            print(f"\n{'UNDEFINED CITATIONS'}")
            print(f"{'-'*60}")
            for cite_key, suggestion in undefined:
                if suggestion:
                    print(f"  ✗ '{cite_key}' → Did you mean '{suggestion}'?")
                else:
                    print(f"  ✗ '{cite_key}' → No match found")
        else:
            print(f"\n✓ ALL CITATIONS VALID - No undefined references!")
    
    return len(undefined) == 0, undefined

def list_keys(bib_file, format='text'):
    """List all BibTeX keys"""
    keys = extract_bibtex_keys(bib_file)
    
    if format == 'latex':
        print("% All valid BibTeX keys (ready for LaTeX)\n")
        for key in sorted(keys.keys()):
            print(f"\\cite{{{key}}}")
    else:
        print(f"BibTeX entries in {bib_file}:\n")
        for key in sorted(keys.keys()):
            print(f"  - {key}")
        print(f"\nTotal: {len(keys)} entries")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: bibtex_validator.py [check|list|missing] <document.tex> <references.bib>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'check':
        if len(sys.argv) < 4:
            print("Usage: bibtex_validator.py check <document.tex> <references.bib>")
            sys.exit(1)
        tex_file = sys.argv[2]
        bib_file = sys.argv[3]
        is_valid, undefined = validate(tex_file, bib_file)
        sys.exit(0 if is_valid else 1)
    
    elif command == 'list':
        if len(sys.argv) < 3:
            print("Usage: bibtex_validator.py list <references.bib> [--format latex]")
            sys.exit(1)
        bib_file = sys.argv[2]
        format_type = 'latex' if '--format' in sys.argv and 'latex' in sys.argv else 'text'
        list_keys(bib_file, format=format_type)
    
    elif command == 'missing':
        if len(sys.argv) < 4:
            print("Usage: bibtex_validator.py missing <document.tex> <references.bib>")
            sys.exit(1)
        tex_file = sys.argv[2]
        bib_file = sys.argv[3]
        validate(tex_file, bib_file, verbose=True)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
