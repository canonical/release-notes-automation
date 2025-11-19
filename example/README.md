# Example materials

This directory contains example materials for the release notes automation process.
This example is intended for release notes for Juju charms.

## File structure

The key components of this directory are:

* `release-notes` -- example files, including:
  * `template` -- folder for templates
  * `artifacts` -- folder for change artifacts
  * `releases` -- folder for release artifacts
  * `common.yaml` -- contains information common for all releases of a given product
  * `***.md` -- generated release notes

## Artifacts

Artifacts are used as a source of data to generate release notes using a Jinja2 template.

Artifact schemas can be adjusted or changed entirely depending on your project's needs and the template used.

See the [example template](release-notes/template/release-template.md.j2).

### Template

A customizable Jinja2 template that defines the format and layout
of the generated release notes.

See
[release-notes/template/release-template.md.j2](release-notes/template/release-template.md.j2)
for example.

### Product information

Product information is similar for all release notes of the same product.
It is stored in the [release-notes/common.yaml](release-notes/common.yaml) file.

File structure:

```yaml
# Human-readable name of the charm
charm_name: ""

# Human-readable condition for the release (revision number, date, etc.)
release_condition: ""

# Boolean to determine whether internal changes will be rendered
show_internal: false
```

### Change artifacts

Individual change artifacts must have names with the format `pr####.yaml`, where
the number represents the pull request associated with the artifact.

File structure:

```yaml
# Version of the artifact schema
version_schema: 1

# The key holding the change(s)
changes:
  - title: "" # What goes into the header. No punctuation please
    author: "" # GitHub profile name
    type: "" # major, minor, deprecated, bugfix, breaking
    description: "" # Brief description of the chage or fix.
    urls: # Relevant URLs
      pr: "" # mandatory link to PR
      related_doc: "" # optional link to related documentation
      related_issue: "" # optional link to related issue
    visibility: public # determines whether artifact should be rendered. Accepted values: public, internal, hidden
    highlight: false # boolean to determine if change is highlight material (i.e. should be featureed in initial paragraph)
```

### Release artifacts

Release artifacts must have names with the format `release####.yaml`, where
the number will be used to tag the output file.

File structure:

```yaml
# --- Information about release ----

# list of change artifacts included in the release
included_changes:

# earliest revision included in the release
earliest_revision:

# latest revision included in the release
latest_revision:

# earliest date included in the release
earliest_date:

# latest date included in the release 
latest_date:
```