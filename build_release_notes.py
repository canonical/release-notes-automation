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

def main():
    """"Generates release notes based on multiple artifacts."""

    # define variables
    artifact_dir = 'artifacts'
    output_dir = 'docs/release-notes'
    release_tag = 'test'
    combined_file = 'all_data.yaml'
    common_file = 'common.yaml'

    # Jinja2 environment 
    env = Environment(loader=FileSystemLoader('template'))
    template = env.get_template('release-template.md.j2')

    # find artifact files
    all_artifact_files = glob.glob(os.path.join(artifact_dir, '*.yaml'))

    if not all_artifact_files:
        print("No artifacts found.")
        return
    
    print(f"Found {len(all_artifact_files)} artifact(s) to process.")

    # check the artifacts to keep
    pr_cutoff = 0 # include everything if not set
    common_data = load_yaml(common_file)
    for key, value in common_data.items():
        if key == "include_prs_after":
            pr_cutoff = value
    # loop through artifacts
    artifact_files = []
    for artifact in all_artifact_files:
        # grab PR number
        substring = artifact[artifact.find('pr')+2:artifact.find('.yaml')]
        pr_num = int(substring)
        if(pr_num > pr_cutoff):
            artifact_files.append(artifact)
        
    print(f"\tUsing {len(artifact_files)} artifact(s) to generate release notes based on pr_cutoff = {pr_cutoff}.\n")

    # add common file to list of files
    artifact_files.append(common_file)

    # generate combined data
    combine_data(artifact_files, combined_file)
    combined_data = load_yaml(combined_file)

    # render template and save
    content = template.render(combined_data)

    output_filename = "release-notes-" + release_tag + ".md"
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, 'w') as f:
        f.write(content)

    print(f"Generated release notes at {output_path}")

    # delete file with all artifacts
    os.remove(combined_file)

if __name__ == '__main__':
    main()