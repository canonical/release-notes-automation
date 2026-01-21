import os
import glob
import yaml
from jinja2 import Environment, FileSystemLoader
import argparse
import re

def load_yaml(file_path):
    """"Loads data from a YAML file."""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)
    
def save_yaml(data, file_path):
    """"Saves data into a YAML file."""
    with open(file_path, 'w') as f:
        yaml.safe_dump(data, f, default_flow_style=False)

def combine_data(file_paths, output_file):
    """"Opens multiple YAML files and combines their data into a single output file."""
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


def is_visible(visibility, show_internal):
    """"Check whether to render a change artifact in the Jinja template."""
    return visibility == "public" or (visibility == "internal" and show_internal)

def check_existing_release_notes(output_path):
    """"Check if release notes file already exists."""
    if os.path.exists(output_path):
        return True
    return False

def main():
    """"Generates release notes based on multiple artifacts."""

    parser = argparse.ArgumentParser(prog="build_release_notes.py", description="Generates release notes based on multiple artifacts")
    parser.add_argument("-a", "--artifactdir", default="docs/release-notes/artifacts", type=str, help = "the directory where your change artifacts live")
    parser.add_argument("-o", "--outputdir", default="docs/release-notes", type=str, help = "the directory where the rendered output will live")
    parser.add_argument("-r", "--releasedir", default="docs/release-notes/releases", type=str, help = "the directory where your release artifacts live")
    parser.add_argument("-c", "--commonfile", default="docs/release-notes/common.yaml", type=str, help = "full path to the YAML file with keys common among all artifacts")
    parser.add_argument("-t", "--templatedir", default="docs/release-notes/template", type=str, help = "directory where your release notes template lives")
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
    env.globals['is_visible'] = is_visible
    template = env.get_template(template_file)

    # find artifact files
    all_artifact_files = glob.glob(os.path.join(artifact_dir, '*.yaml'))

    if not all_artifact_files:
        print("No change artifacts found.")
        return
    
    print(f"Found {len(all_artifact_files)} change artifact(s) in database.")

    # find release artifact
    release_files = glob.glob(os.path.join(release_dir, '*.yaml'))

    if not release_files:
        print("No release artifacts found.")
        return
    
    print(f"Found {len(release_files)} release artifact(s) in database.")

    release_artifact_pattern = re.compile(r"release(\d+)\.(yaml|yml)$")

    release_file = max(
        release_files,
        key=lambda f: int(release_artifact_pattern.search(f).group(1)),
    )

    if not release_file:
        print("No matching release file found.")
        return

    release_tag = release_artifact_pattern.search(release_file).group(1)

    print(f"Found release artifact {release_file} based on tag {release_tag}.")

    # check if release notes already exist
    output_filename = "release-notes-" + release_tag + ".md"
    output_path = os.path.join(output_dir, output_filename)
    
    if check_existing_release_notes(output_path):
        print(f"Warning: Release notes already exist at {output_path}")

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

    with open(output_path, 'w') as f:
        f.write(content)

    print(f"Generated release notes at {output_path}")

    # delete file with all artifacts
    os.remove(combined_file)

if __name__ == '__main__':
    main()

