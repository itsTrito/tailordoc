# cv

## How to use

### run.sh

```bash
Usage: ./run.sh [-k] [-s]
Options:
  -k   Enable keeping the generated folder after usage
  -s   Enable silent mode. (Less verbose)
```

### process_file.py

```
Usage: python process_file.py <yaml_file_path> <input_file_path> <output_file_path>
```

- <yaml_file_path> is config file
- <input_file_path> is the file you want to process
- <output_file_path> is the name you want for the outputed file

### Config files

You can create as much config yaml files in the ./configs directory. It will generate an output file for each of them (if you use the run.sh) it will also generate a file for each lang specified in the config file.

```yaml
# Var section let's you override some necessary variables
# All optionals
var:
  input: "jack.tex"
  comment_symbol: "%"
# -------------------------
# Chapters section let's you choose which part of the document will stay and which will be removed
chapters:
  experience: true
  education: true
# -------------------------
# Langs section is like the chapters' section but it will create a new document for each lang
langs:
  english: true
  french: true
```

### Res files

On runtime, every file in the ./res directory will be copied in the ./generated folder so that they can be used by the intermediary files.

### Editing

You can use any tag with the following synthax

```latex
%<*tag> opens the section
Anyting between the two will be considered as part of the section.
In works for both chapters and langs
%</tag> closes the section
%<tag> Will consider everything on the same line as part of the section

For langs the 2 first characters are also accepted
%<english> is fine
%<en> is also fine

% The comment symbol can be overriden to be use with other languages
```

### Latex

If you're using it with latex you'll need to install latex first. Make sure you can use the pdflatex command.

### Credit

The sample Latex project is from https://github.com/latex-ninja/simple-hipstercv/. All credit to latex-ninja
