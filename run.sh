#!/bin/bash

CONFIG_DIR="configs"
MAIN_TEX="main.tex"
OUT_DIR="out"
AUX_DIR="auxil"

for yaml_file in $CONFIG_DIR/*.yaml; do
    if [ -f "$yaml_file" ]; then
        filename=$(basename -- "$yaml_file")
        filename_noext="${filename%.*}"

        output_tex="generated_${filename_noext}.tex"

        python process_file.py "$yaml_file" "$MAIN_TEX" "$output_tex"

        pdflatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf -output-directory="$OUT_DIR" -aux-directory="$AUX_DIR" -jobname="$filename_noext" "$output_tex" > /dev/null
        echo "Published $filename_noext.pdf from $output_tex"
    fi
done
