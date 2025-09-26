#!/bin/bash

# Install PyNIDM from the skip_annotation branch
# This branch allows skipping the annotation step

set -euo pipefail

echo "Installing PyNIDM from skip_annotation branch..."

# First uninstall any existing PyNIDM to avoid conflicts
echo "Uninstalling any existing PyNIDM..."
micromamba run -n simple2 python -m pip uninstall -y pynidm 2>/dev/null || true

# Install from the specific branch
echo "Installing from djarecka/PyNIDM skip_annotation branch..."
micromamba run -n simple2 python -m pip install --force-reinstall --no-deps git+https://github.com/djarecka/PyNIDM.git@skip_annotation

# Install dependencies if needed
echo "Installing dependencies..."
micromamba run -n simple2 python -m pip install rdflib prov pydot graphviz click

echo "Installation complete!"
echo "Checking installation..."

# Verify installation
micromamba run -n simple2 python -c "import pynidm; print(f'PyNIDM installed successfully')" || echo "PyNIDM module check failed"

# Check if bidsmri2nidm is available
micromamba run -n simple2 which bidsmri2nidm && echo "bidsmri2nidm found"

echo "Done!"