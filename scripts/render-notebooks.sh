#!/bin/bash
# scripts/render-notebooks.sh
# Renders .ipynb files from public/notebooks/ to public/notebooks/rendered/

SOURCE_DIR="public/notebooks"
OUTPUT_DIR="public/notebooks/rendered"

mkdir -p "$OUTPUT_DIR"

for nb in "$SOURCE_DIR"/*.ipynb; do
  [ -f "$nb" ] || continue
  jupyter nbconvert --to html \
    --template classic \
    --output-dir "$OUTPUT_DIR" \
    "$nb"
  echo "Rendered: $nb"
done

echo "Done. Check $OUTPUT_DIR/ for rendered HTML files."
