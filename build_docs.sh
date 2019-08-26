#!/bin/bash

sudo_askpass="$(command -v ssh-askpass)"
export SUDO_ASKPASS="${sudo_askpass}"
export NO_AT_BRIDGE=1  # get rid of (ssh-askpass:25930): dbind-WARNING **: 18:46:12.019: Couldn't register with accessibility bus: Did not receive a reply.


function set_lib_bash_permissions {
    local user
    user="$(printenv USER)"
    $(command -v sudo 2>/dev/null) chmod -R 0755 "/usr/local/lib_bash"
    $(command -v sudo 2>/dev/null) chmod -R +x /usr/local/lib_bash/*.sh
    $(command -v sudo 2>/dev/null) chown -R root /usr/local/lib_bash || "$(command -v sudo 2>/dev/null)" chown -R "${user}" /usr/local/lib_bash || echo "giving up set owner" # there is no user root on travis
    $(command -v sudo 2>/dev/null) chgrp -R root /usr/local/lib_bash || "$(command -v sudo 2>/dev/null)" chgrp -R "${user}" /usr/local/lib_bash || echo "giving up set group" # there is no user root on travis
}


function install_lib_bash {
    echo "installing lib_bash"
    $(command -v sudo 2>/dev/null) rm -fR /usr/local/lib_bash
    $(command -v sudo 2>/dev/null) git clone https://github.com/bitranox/lib_bash.git /usr/local/lib_bash > /dev/null 2>&1
    set_lib_bash_permissions
}



function install_or_update_lib_bash {
    if [[ -f "/usr/local/lib_bash/install_or_update.sh" ]]; then
        # file exists - so update
        $(command -v sudo 2>/dev/null) /usr/local/lib_bash/install_or_update.sh
    else
        install_lib_bash
    fi
}

install_or_update_lib_bash


function include_dependencies {
    source /usr/local/lib_bash/lib_color.sh
    source /usr/local/lib_bash/lib_retry.sh
    source /usr/local/lib_bash/lib_helpers.sh
}

include_dependencies


### CONSTANTS
codeclimate_link_hash="ff3f414903627e5cfc35"
# TRAVIS_TAG


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
rst_include -h > ./.docs/rst_include_help_output.txt
rst_include include -h > ./.docs/rst_include_help_include_output.txt
rst_include replace -h > ./.docs/rst_include_help_replace_output.txt

clr_green "import the include blocks"
rst_include include -s ./.docs/README_template.rst -t ./README.rst

clr_green "replace repository strings"

# please note that the replace syntax is not shown correctly in the README.rst,
# because it gets replaced itself by the build_docs.py
# we could overcome this by first replacing, and afterwards including -
# check out the build_docs.sh for the correct syntax !

# example for piping
cat ./README.rst \
    | rst_include --inplace replace "{repository_slug}" "${TRAVIS_REPO_SLUG}" \
    | rst_include --inplace replace "{repository}" "${repository}" \
    | rst_include --inplace replace "{repository_dashed}" "${repository_dashed}" \
    | rst_include --inplace replace "{codeclimate_link_hash}" "${codeclimate_link_hash}" \
     > ./README.rst

clr_green "done"
clr_green "******************************************************************************************************************"
clr_bold clr_green "FINISHED building README.rst"
clr_green "******************************************************************************************************************"
