#!/usr/bin/env python3

import csv
import json
import sys
import copy

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

# Read ABIDE1 JSON mapping
with open('data/mappings/abide_phenotypic_v1_0b_vars_to_terms_v5.json', 'r') as f:
    abide1_mapping = json.load(f)

# Create a mapping from ABIDE1 variable names to their JSON entries
abide1_var_to_entry = {}
for key, value in abide1_mapping.items():
    if "variable='" in key:
        var_name = key.split("variable='")[1].split("'")[0]
        abide1_var_to_entry[var_name] = (key, value)

# Convert to lowercase for case-insensitive comparison
abide1_lower = {h.lower(): h for h in abide1_headers}
abide2_lower = {h.lower(): h for h in abide2_headers}

# Create the new ABIDE2 mapping
abide2_mapping = {}

# First, handle overlapping variables
mapped_count = 0
for a2_lower, a2_orig in abide2_lower.items():
    if a2_lower in abide1_lower:
        a1_orig = abide1_lower[a2_lower]

        # Check if this ABIDE1 variable has a mapping
        if a1_orig in abide1_var_to_entry:
            # Deep copy the entire ABIDE1 mapping entry
            _, entry = abide1_var_to_entry[a1_orig]
            entry_copy = copy.deepcopy(entry)

            # Update only the source_variable to use ABIDE2's name
            entry_copy['source_variable'] = a2_orig

            # Create the key for ABIDE2 - simplified without source=
            key = f"DD(variable='{a2_orig}')"
            abide2_mapping[key] = entry_copy
            mapped_count += 1
            print(f"Mapped {a2_orig} -> {a1_orig} (with type: {entry_copy.get('valueType', 'N/A')})")

print(f"\nTotal overlapping variables mapped: {mapped_count}")

# Now handle ABIDE2-only variables with minimal mappings
all_matched_a2 = set()
for a2_lower, a2_orig in abide2_lower.items():
    if a2_lower in abide1_lower:
        all_matched_a2.add(a2_orig)

abide2_only = [h for h in abide2_headers if h not in all_matched_a2]

print(f"\nCreating minimal mappings for {len(abide2_only)} ABIDE2-only variables...")

for var in abide2_only:
    # Create the key for ABIDE2 - simplified without source=
    key = f"DD(variable='{var}')"

    # For ABIDE2-only variables, create a minimal mapping
    # Just the essentials: label, source_variable, and associatedWith
    abide2_mapping[key] = {
        "label": var,  # Keep original ABIDE2 variable name
        "source_variable": var,
        "associatedWith": "NIDM"
    }

print(f"\nTotal variables in ABIDE2 mapping: {len(abide2_mapping)}")

# Write the output JSON
output_path = 'data/mappings/abide2_phenotypic_vars_to_terms.json'
with open(output_path, 'w') as f:
    json.dump(abide2_mapping, f, indent=4)

print(f"\nABIDE2 mapping JSON written to: {output_path}")
print(f"Total mappings created: {len(abide2_mapping)}")
print(f"  - Overlapping with ABIDE1 (full copy): {mapped_count}")
print(f"  - ABIDE2-only (minimal): {len(abide2_only)}")