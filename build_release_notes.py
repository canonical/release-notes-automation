import os
import glob
import yaml
from jinja2 import Environment, FileSystemLoader

def load_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)
    
def save_yaml(data, file_path):
    with open(file_path, 'w') as f:
        yaml.safe_dump(data, f, default_flow_style=False)

def combine_data(file_paths, output_file):
    combined_data = {}

    for file_path in file_paths:
        data = load_yaml(file_path)
        for key, value in data.items():
            if key in combined_data:
                if isinstance(combined_data[key], list) and isinstance(value, list):
                    combined_data[key].extend(value)
                elif isinstance(combined_data[key], list):
                    combined_data[key].append(value)
                elif isinstance(value, list):
                    combined_data[key] = [combined_data[key]] + value
                else:
                    combined_data[key] = [combined_data[key], value]
            else:
                combined_data[key] = value

    save_yaml(combined_data, output_file)

def filter_by_tag(files, tag):
    files_with_tag = []
    for file in files:
        data = load_yaml(file)
        if tag == data.get('change')[0].get('release_tag'):
            files_with_tag.append(file)

    return files_with_tag

def main():
    """"Generates release notes based on multiple artifacts."""

    # define variables
    artifact_dir = 'artifacts'
    output_dir = 'docs/release-notes'
    release_tag = 'rev1-split'
    output_file = 'all_data.yaml'
    common_file = 'common.yaml'

    # Jinja2 environment 
    env = Environment(loader=FileSystemLoader('template'))
    template = env.get_template('release-template.md.j2')

    # find artifact files
    artifact_files = glob.glob(os.path.join(artifact_dir, '*.yaml'))

    if not artifact_files:
        print("No artifacts found.")
        return
    
    print(f"Found {len(artifact_files)} artifact(s) to process.")

    # only keep artifact_files with the correct release_tag
    # artifact_files = filter_by_tag(artifact_files, release_tag)
    # print(f"Found {len(artifact_files)} artifact(s) with release tag {release_tag}.")

    # add common file to list of files
    artifact_files.append(common_file)

    # generate combined data
    combine_data(artifact_files, output_file)
    combined_data = load_yaml(output_file)

    # render template and save
    content = template.render(combined_data)

    output_filename = "release-notes-" + release_tag + ".md"
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, 'w') as f:
        f.write(content)

    print(f"Generated release notes at {output_path}")


if __name__ == '__main__':
    main()