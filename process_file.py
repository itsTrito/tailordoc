import yaml
import re
import os
import sys

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data
    
def read_file(file_path):
    with open(file_path, 'r') as file:
            content = file.read()

    return content

def process_content(content, key, remove_tags, comment_key):
    start_tag = f"{comment_key}<\*{key}>"
    end_tag = f"{comment_key}<\/{key}>"
    inline_tag = f"{comment_key}<{key}>"

    if remove_tags:
        # Remove tags and content between them
        content = re.sub(f'{start_tag}.*?{end_tag}', '', content, flags=re.DOTALL)
        content = re.sub(f'{inline_tag}.*\n', '', content)
    else:
        # Replace tags with their content
        content = re.sub(f'{start_tag}(.*?){end_tag}', r'\1', content, flags=re.DOTALL)
        content = re.sub(f'{inline_tag}(.*)\n', r'\1\n', content)
        
    return content

def process_file(yaml_config_file_path, default_input_file_path, output_file_path, yaml_data, comment_key):

    input_file_path = default_input_file_path

    # Var handling
    if yaml_data['var'] != None:
        if 'input' in yaml_data['var']:
            input_file_path = yaml_data['var']['input']
        if 'comment_symbol' in yaml_data['var']:
            comment_key = yaml_data['var']['comment_symbol']

    content = read_file(input_file_path)

    # Chapters handling
    if yaml_data['chapters'] != None:
        for key, value in yaml_data['chapters'].items():
            if value is False:
                content = process_content(content, key, True, comment_key=comment_key)  # Set True to remove tags
            else:
                content = process_content(content, key, False, comment_key=comment_key)

    # Langs handling
    if yaml_data['langs'] != None:
        for key, value in yaml_data['langs'].items():
            localized_content = content
            sub_key = key[:2]
            if value is True:
                for other_key, _ in yaml_data['langs'].items():
                    other_sub_key = other_key[:2]
                    localized_content = process_content(localized_content, other_key, key != other_key, comment_key=comment_key)
                    localized_content = process_content(localized_content, other_sub_key, sub_key != other_sub_key, comment_key=comment_key)
                tab = str.split(output_file_path, ".")
                new_file_path = tab[0] + "_" + sub_key + "." + tab[1]
                make_file(yaml_config_file_path, input_file_path, new_file_path, localized_content)
    else:
        make_file(yaml_config_file_path, input_file_path, output_file_path, content)

def make_file(yaml_config_file_path, input_file_path, output_file_path, content):     
    output_directory, _ = os.path.split(output_file_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist
    
    with open(output_file_path, 'w+') as output_file:
        output_file.write(content)
        print(f"Generated {output_file_path} from {input_file_path} and {yaml_config_file_path}")


comment_symbol = "%"

def main(yaml_config_file_path, input_file_path, output_file_path):
    # Reading values from YAML file
    yaml_data = read_yaml(yaml_config_file_path)
    process_file(yaml_config_file_path, input_file_path, output_file_path, yaml_data, comment_key=comment_symbol)

# main
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python process_file.py <yaml_file_path> <input_file_path> <output_file_path>")
        sys.exit(1)

    yaml_file_path = sys.argv[1]
    input_file_path = sys.argv[2]
    output_file_path = sys.argv[3]

    main(yaml_file_path, input_file_path, output_file_path)
