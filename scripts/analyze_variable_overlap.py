#!/usr/bin/env python3

import csv
import json

# Read ABIDE2 TSV headers
with open('data/phenotypes/ABIDEII-BNI_1_participants.tsv', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    abide2_headers = next(reader)
    # Remove any trailing spaces from headers
    abide2_headers = [h.strip() for h in abide2_headers]

# Read ABIDE1 CSV headers
with open('data/phenotypes/Phenotypic_V1_0b.csv', 'r') as f:
    reader = csv.reader(f)
    abide1_headers = next(reader)

# Read ABIDE1 JSON mapping to get the mapped variables
with open('data/mappings/abide_phenotypic_v1_0b_vars_to_terms_v5.json', 'r') as f:
    abide1_mapping = json.load(f)

# Extract just the variable names from the JSON keys
abide1_mapped_vars = set()
for key in abide1_mapping.keys():
    # Extract variable name from keys like "DD(source='Phenotypic_V1_0b.csv', variable='SITE_ID')"
    if "variable='" in key:
        var_name = key.split("variable='")[1].split("'")[0]
        abide1_mapped_vars.add(var_name)

print("=" * 80)
print("ABIDE1 variables (from CSV):")
print(f"Total: {len(abide1_headers)}")
print("Variables:", abide1_headers)
print()

print("=" * 80)
print("ABIDE2 variables (from TSV):")
print(f"Total: {len(abide2_headers)}")
print("First 20 variables:", abide2_headers[:20])
print()

# Convert to lowercase for case-insensitive comparison
abide1_lower = {h.lower(): h for h in abide1_headers}
abide2_lower = {h.lower(): h for h in abide2_headers}

# Find exact matches (case-insensitive)
exact_matches = []
for a2_lower, a2_orig in abide2_lower.items():
    if a2_lower in abide1_lower:
        exact_matches.append((a2_orig, abide1_lower[a2_lower]))

print("=" * 80)
print("EXACT MATCHES (case-insensitive):")
print(f"Total: {len(exact_matches)}")
for a2, a1 in exact_matches:
    print(f"  ABIDE2: {a2:30} -> ABIDE1: {a1}")
print()

# Find close matches (with/without underscores, spaces)
close_matches = []
for a2_lower, a2_orig in abide2_lower.items():
    # Normalize: remove spaces and underscores
    a2_norm = a2_lower.replace('_', '').replace(' ', '').replace('-', '')

    for a1_lower, a1_orig in abide1_lower.items():
        a1_norm = a1_lower.replace('_', '').replace(' ', '').replace('-', '')

        if a2_norm == a1_norm and (a2_orig, a1_orig) not in exact_matches:
            close_matches.append((a2_orig, a1_orig))

print("=" * 80)
print("CLOSE MATCHES (ignoring spaces, underscores, hyphens):")
print(f"Total: {len(close_matches)}")
for a2, a1 in close_matches:
    print(f"  ABIDE2: {a2:30} -> ABIDE1: {a1}")
print()

# Find ABIDE2-only variables
all_matched_a2 = set([a2 for a2, _ in exact_matches + close_matches])
abide2_only = [h for h in abide2_headers if h not in all_matched_a2]

print("=" * 80)
print("ABIDE2-ONLY VARIABLES:")
print(f"Total: {len(abide2_only)}")
for i in range(0, min(50, len(abide2_only))):
    print(f"  {abide2_only[i]}")
if len(abide2_only) > 50:
    print(f"  ... and {len(abide2_only) - 50} more")