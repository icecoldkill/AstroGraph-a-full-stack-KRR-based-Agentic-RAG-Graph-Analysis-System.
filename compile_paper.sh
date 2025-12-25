#!/bin/bash

# Compilation script for IEEE paper
# This script compiles the GSE_KG_IEEE_Paper.tex file with proper formatting

echo "Compiling IEEE Paper for Global Space Exploration Knowledge Graph..."

# Check if pdflatex is installed
if ! command -v pdflatex &> /dev/null; then
    echo "Error: pdflatex is not installed. Please install a LaTeX distribution."
    exit 1
fi

# Compile the paper (multiple passes for proper references)
echo "First compilation pass..."
pdflatex GSE_KG_IEEE_Paper.tex

if [ $? -ne 0 ]; then
    echo "Error: First compilation pass failed."
    exit 1
fi

echo "Second compilation pass (for cross-references)..."
pdflatex GSE_KG_IEEE_Paper.tex

if [ $? -ne 0 ]; then
    echo "Error: Second compilation pass failed."
    exit 1
fi

echo "Third compilation pass (final)..."
pdflatex GSE_KG_IEEE_Paper.tex

if [ $? -ne 0 ]; then
    echo "Error: Third compilation pass failed."
    exit 1
fi

# Clean up auxiliary files
echo "Cleaning up auxiliary files..."
rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot *.fdb_latexmk *.fls *.synctex.gz

echo "Compilation complete! Output file: GSE_KG_IEEE_Paper.pdf"

# Check if PDF was created
if [ -f "GSE_KG_IEEE_Paper.pdf" ]; then
    echo "✅ PDF successfully generated!"
    echo "File size: $(du -h GSE_KG_IEEE_Paper.pdf | cut -f1)"
else
    echo "❌ PDF generation failed!"
    exit 1
fi
