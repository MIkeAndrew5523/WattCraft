#!/bin/bash
# scripts/render-notebooks.sh
# Usage: ./scripts/render-notebooks.sh [notebook-name.ipynb]
# Renders one or all notebooks in /notebooks/source/ to /notebooks/rendered/

NOTEBOOK=$1
SOURCE_DIR="notebooks/source"
OUTPUT_DIR="notebooks/rendered"

if [ -z "$NOTEBOOK" ]; then
  # Render all notebooks
  for nb in $SOURCE_DIR/*.ipynb; do
    jupyter nbconvert --to html \
      --template classic \
      --output-dir $OUTPUT_DIR \
      "$nb"
    echo "Rendered: $nb"
  done
else
  jupyter nbconvert --to html \
    --template classic \
    --output-dir $OUTPUT_DIR \
    "$SOURCE_DIR/$NOTEBOOK"
fi

echo "Done. Check $OUTPUT_DIR/ for rendered HTML files."
