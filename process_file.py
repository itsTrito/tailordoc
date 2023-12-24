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

def process_content(content, key, remove_tags):
    start_tag = f"%<\*{key}>"
    end_tag = f"%<\/{key}>"
    inline_tag = f"%<{key}>"

    if remove_tags:
        # Remove tags and content between them
        content = re.sub(f'{start_tag}.*?{end_tag}', '', content, flags=re.DOTALL)
        content = re.sub(f'{inline_tag}.*\n', '', content)
    else:
        # Replace tags with their content
        content = re.sub(f'{start_tag}(.*?){end_tag}', r'\1', content, flags=re.DOTALL)
        content = re.sub(f'{inline_tag}(.*)\n', r'\1\n', content)
        
    return content

def main(yaml_config_file_path, input_file_path, output_file_path):
    # Reading values from YAML file
    yaml_data = read_yaml(yaml_config_file_path)
    
    if 'params' in yaml_data:
        content = read_file(input_file_path)
        for key, value in yaml_data['params'].items():
            if value is False:
                content = process_content(content, key, True)  # Set True to remove tags
            else:
                content = process_content(content, key, False)
                
        output_directory, _ = os.path.split(output_file_path)
        if output_directory:
            os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist
        
        with open(output_file_path, 'w+') as output_file:
            output_file.write(content)
            print(f"Generated {output_file_path} from {input_file_path} and {yaml_config_file_path}")

# main
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python process_file.py <yaml_file_path> <input_file_path> <output_file_path>")
        sys.exit(1)

    yaml_file_path = sys.argv[1]
    input_file_path = sys.argv[2]
    output_file_path = sys.argv[3]

    main(yaml_file_path, input_file_path, output_file_path)
