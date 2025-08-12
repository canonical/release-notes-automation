import os
import glob
import yaml
from jinja2 import Environment, FileSystemLoader
import argparse

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

    parser = argparse.ArgumentParser(prog="build_release_notes.py", description="Generates release notes based on multiple artifacts")
    parser.add_argument("-a", "--artifactdir", default="artifacts", type=str, help = "the directory where your change artifacts live")
    parser.add_argument("-o", "--outputdir", default="docs/release-notes", type=str, help = "the directory where the rendered output will live")
    parser.add_argument("-r", "--releasedir", default="releases", type=str, help = "the directory where your release artifacts live")
    parser.add_argument("-c", "--commonfile", default="common.yaml", type=str, help = "full path to your common.yaml file")
    parser.add_argument("-t", "--templatedir", default="template", type=str, help = "directory where your release notes template lives")
    parser.add_argument("-f", "--templatefile", default="release-template.md.j2", type=str, help = "name of release notes template file")
    args = parser.parse_args()

    # define variables
    artifact_dir = args.artifactdir
    output_dir = args.outputdir
    release_dir = args.releasedir
    common_file = args.commonfile
    template_dir = args.templatedir
    template_file = args.templatefile
    combined_file = 'all_data.yaml'

    # Jinja2 environment 
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    # find artifact files
    all_artifact_files = glob.glob(os.path.join(artifact_dir, '*.yaml'))

    if not all_artifact_files:
        print("No change artifacts found.")
        return
    
    print(f"Found {len(all_artifact_files)} artifact(s) in database.")

    # find release artifact
    release_files = glob.glob(os.path.join(release_dir, '*.yaml'))

    if not release_files:
        print("No release artifacts found.")
        return
    
    # get the most recently created release artifact
    release_file = max(release_files, key=os.path.getctime)

    if not release_file:
        print("No matching release file found.")
        return

    release_tag = release_file[release_file.find('.yaml')-4:release_file.find('.yaml')]

    print(f"Found release artifact {release_file} based on tag {release_tag}.")

    release_data = load_yaml(release_file)
    included_changes = release_data.get("included_changes", [])
    
    if not included_changes:
        print("No change artifacts included in this release.")
        return
    
    # loop through artifacts
    artifact_files = []
    for artifact in all_artifact_files:
        # grab PR number
        substring = artifact[artifact.find('.yaml')-6:]
        if any(substring in change for change in included_changes):
            artifact_files.append(artifact)

    if not artifact_files:
        print("No relevant change artifacts found for this release.")
        return

    print(f"Found {len(artifact_files)} artifact(s) for this release.")

    # add release artifact to list of files
    artifact_files.append(release_file)

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