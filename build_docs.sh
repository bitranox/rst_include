#!/bin/bash

### CONSTANTS
codeclimate_link_hash="ff3f414903627e5cfc35"
# TRAVIS_TAG

function include_dependencies {
    local my_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"  # this gives the full path, even for sourced scripts
    chmod +x "${my_dir}"/lib_bash/*.sh
    source "${my_dir}/lib_bash/lib_color.sh"
}

include_dependencies  # we need to do that via a function to have local scope of my_dir

function check_repository_name {
    if [[ -z ${TRAVIS_REPO_SLUG} ]]
        then
            clr_bold clr_red "ERROR no travis repository name set - exiting"
            exit 1
        fi
}

clr_bold clr_green "Build README.rst for repository: ${TRAVIS_REPO_SLUG}"

check_repository_name

repository="${TRAVIS_REPO_SLUG#*/}"                                 # "username/repository_name" --> "repository_name"
repository_dashed="$( echo -e "$repository" | tr  '_' '-'  )"       # "repository_name --> repository-name"

clr_green "create the sample help outputs"
rst_inc -h > ./docs/rst_include_help_output.txt
rst_inc include -h > ./docs/rst_include_help_include_output.txt
rst_inc replace -h > ./docs/rst_include_help_replace_output.txt

clr_green "import the include blocks"
rst_inc include -s ./docs/README_template.rst -t ./docs/README_template_included.rst

clr_green "replace repository strings"

# please note that the replace syntax is not shown correctly in the README.rst,
# because it gets replaced itself by the build_docs.py
# we could overcome this by first replacing, and afterwards including -
# check out the build_docs.sh for the correct syntax !

# example for piping
cat ./docs/README_template_included.rst \
    | rst_inc replace "{repository_slug}" "${TRAVIS_REPO_SLUG}" \
    | rst_inc replace "{repository}" "${repository}" \
    | rst_inc replace "{repository_dashed}" "${repository_dashed}" \
    | rst_inc replace "{codeclimate_link_hash}" "${codeclimate_link_hash}" \
     > ./README.rst

clr_green "cleanup"
rm ./docs/README_template_included.rst

clr_green "done"
clr_green "******************************************************************************************************************"
clr_bold clr_green "FINISHED building README.rst"
clr_green "******************************************************************************************************************"
