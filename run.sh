#!/bin/bash

CONFIG_DIR="configs"
MAIN_TEX="main.tex"
OUT_DIR="out"
AUX_DIR="auxil"
GENERATED_DIR="generated"
RES_DIR="res"

# Set default value for the flag
keep_generated=false
silent=false

# Define a usage function to display information about script usage
usage() {
    echo "Usage: $0 [-k] [-s]"
    echo "Options:"
    echo "  -k   Enable keeping the $GENERATED_DIR folder after usage"
    echo "  -s   Enable silent mode. (Less verbose)"
    exit 1
}

# Parse command-line options
while getopts ":ks" opt; do
  case ${opt} in
    k )
      keep_generated=true
      ;;
    s )
      silent=true
      ;;
    \? )
      echo "Invalid option: $OPTARG" 1>&2
      usage
      ;;
  esac
done
shift $((OPTIND -1))

# Check if the directory exists
if [ ! -d "$OUT_DIR" ]; then
    # Create the directory if it doesn't exist
    mkdir -p "$OUT_DIR"
    echo "Directory '$OUT_DIR' created."
fi

# Check if the directory exists
if [ ! -d "$AUX_DIR" ]; then
    # Create the directory if it doesn't exist
    mkdir -p "$AUX_DIR"
    echo "Directory '$AUX_DIR' created."
fi

# Check if the directory exists
if [ ! -d "$GENERATED_DIR" ]; then
    # Create the directory if it doesn't exist
    mkdir -p "$GENERATED_DIR"
    echo "Directory '$GENERATED_DIR' created."
fi

cp -r ${RES_DIR}/* ${GENERATED_DIR}/

for yaml_file in $CONFIG_DIR/*.yaml; do
    if [ -f "$yaml_file" ]; then
        filename=$(basename -- "$yaml_file")
        filename_noext="${filename%.*}"

        output_tex="${GENERATED_DIR}/generated_${filename_noext}.tex"

        python process_file.py "$yaml_file" "$MAIN_TEX" "$output_tex"
    fi
done

cd $GENERATED_DIR
for generated_tex_file in generated_*.tex; do
    if [ -f "$generated_tex_file" ]; then
        filename=$(basename -- "$generated_tex_file")
        filename_noext="${filename%.*}"
        output=$(echo "$filename_noext" | sed 's/generated_//')
        if [ "$silent" = true ]; then
            pdflatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf -output-directory="../$OUT_DIR" -aux-directory="../$AUX_DIR" -jobname="$output" "$generated_tex_file" > /dev/null
            echo "Published $output.pdf from $filename"
        else
            pdflatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf -output-directory="../$OUT_DIR" -aux-directory="../$AUX_DIR" -jobname="$output" "$generated_tex_file"
            echo "Published $output.pdf from $filename"
        fi
    fi
done

cd ..

if [ "$keep_generated" = false ]; then
  rm -r $GENERATED_DIR
fi
