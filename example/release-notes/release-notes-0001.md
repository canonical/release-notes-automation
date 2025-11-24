<!-- Remember to update this file for your charm!! -->

# Fake release notes – latest/stable

These release notes cover new features and changes in Fake for revisions
1-8 between the dates of 2025-01-01 and 2025-06-01.

Main features:

* Added initial Python script.
* Added GitHub action.


Main breaking changes:

* Renamed feature tag.


Main bug fixes:
* Fixed a bug where the URLs weren't rendered correctly in the template.
* Fixed a bug where the automation script incorrectly named the output file.


See our [Release policy and schedule](docs/release-notes/landing-page.md).

## Requirements and compatibility

<!--
Specify the workload version; link to the workload's release notes if available.

Add information about the requirements for this charm in the table
below, for instance, a minimum Juju version. 

If the user will need any specific upgrade instructions for this
release, include those instructions here.
-->

The charm operates <workload name with version>.

The table below shows the required or supported versions of the software necessary to operate the charm.

| Software                | Required version |
|-------------------------|------------------|
| Juju                    | XXXX             |
| Terraform               | XXXX             |
| Terraform Juju provider | XXXX             |
| Ubuntu                  | XXXX             |
| XXXX                    | XXXX             |

## Updates

The following major and minor features were added in this release.

### Added initial Python script
Added initial automation script to build release notes.
<Add more context and information about the entry>

Relevant links:
* [PR](https://github.com/erinecon/automation-testing-changelog-release-notes/commit/15716db0e2c5f19124fd32f9a26d14126bbc9ca0)


### Added initial Jinja template.
First test of the Jinja template.
<Add more context and information about the entry>

Relevant links:
* [PR](https://github.com/erinecon/automation-testing-changelog-release-notes/commit/cbd08aa188b113439c2907e6ae108e080399b3b0)


### Added GitHub action
Now there's a GitHub action that uses the script and automatically opens a pull
request with the rendered release notes!

<Add more context and information about the entry>

Relevant links:
* [PR](https://github.com/erinecon/automation-testing-changelog-release-notes/pull/2)





## Breaking changes

The following backwards-incompatible changes are included in this release.

### Renamed feature tag
Renamed `feature_tag` to `release_tag`.
<Add more context and information about the entry>

Relevant links:
* [PR](https://github.com/erinecon/automation-testing-changelog-release-notes/commit/85abffb0fc3ca2b6a33e62d28be62349f052b041)


## Bug fixes

* Fixed a bug where the URLs weren't rendered correctly in the template ([PR](https://github.com/erinecon/automation-testing-changelog-release-notes/commit/3de734d1f1993d1f56d4f6c6cf9c8f74a6b08ec8)).
* Fixed feature tag grabbing ([PR](https://github.com/erinecon/automation-testing-changelog-release-notes/commit/50e8f331c1f776483d89d8c7d1e23706e40ba7f4)).
* Fixed a bug where the automation script incorrectly named the output file ([PR](https://github.com/erinecon/automation-testing-changelog-release-notes/commit/ac0e0db5a810321e64e5b719199b53a0376d08e0)).



## Deprecated

The following features have been deprecated.

### Removed release_tag from the artifact
Removed `release_tag` from the artifact.
<Add more context and information about the entry>

Relevant links:
* [PR](https://github.com/erinecon/automation-testing-changelog-release-notes/commit/99bf42cbb0f819860e3ca9e8c1058ea006c753da)


## Known issues

<!--
Add a bulleted list with links to unresolved issues – the most important/pressing ones,
the ones being worked on currently, or the ones with the most visibility/traffic.
You don’t need to add links to all the issues in the repository if there are
several – a list of 3-5 issues is sufficient. 
If there are no known issues, keep the section and write "No known issues".
-->

## Thanks to our contributors

<!--
List of contributors based on PRs/commits. Remove this section if there are no contributors in this release.
-->

[erinecon](https://github.com/erinecon)