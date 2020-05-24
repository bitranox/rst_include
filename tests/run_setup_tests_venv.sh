#!/bin/bash

sudo_askpass="$(command -v ssh-askpass)"
export SUDO_ASKPASS="${sudo_askpass}"
export NO_AT_BRIDGE=1  # get rid of (ssh-askpass:25930): dbind-WARNING **: 18:46:12.019: Couldn't register with accessibility bus: Did not receive a reply.

sleeptime_on_error=5


# shellcheck disable=SC2164  # no check if cd fails
own_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"  # this gives the full path, even for sourced scripts
pytest_root_dir="$(dirname "${own_dir}")"                   # one level up
# if we have other Projects stored in that directory, we can import them without installing, otherwise not harmful
projects_dir="$(dirname "${pytest_root_dir}")"              # one level up
export PYTHONPATH="${projects_dir}":"${PYTHONPATH}"
# if we have other Projects stored in that directory, we can import them without installing, otherwise not harmful
projects_dir_upper="$(dirname "${projects_dir}")"              # one level up
export PYTHONPATH="${projects_dir_upper}":"${PYTHONPATH}"


function install_or_update_lib_bash {
    if [[ ! -f /usr/local/lib_bash/install_or_update.sh ]]; then
        "$(command -v sudo 2>/dev/null)" git clone https://github.com/bitranox/lib_bash.git /usr/local/lib_bash 2>/dev/null
        "$(command -v sudo 2>/dev/null)" chmod -R 0755 /usr/local/lib_bash 2>/dev/null
        "$(command -v sudo 2>/dev/null)" chmod -R +x /usr/local/lib_bash/*.sh 2>/dev/null
        "$(command -v sudo 2>/dev/null)" /usr/local/lib_bash/install_or_update.sh 2>/dev/null
    else
        /usr/local/lib_bash/install_or_update.sh
    fi
}

install_or_update_lib_bash

source /usr/local/lib_bash/lib_helpers.sh

function clean_caches {
    # mypy and pytest caches should be deleted, because sometimes problems on collecting if not
    local pytest_root_dir=$1
    clr_green "clean pytest and mypy caches"
    "$(command -v sudo 2>/dev/null)" find "${pytest_root_dir}" -name .mypy_cache -type d -exec rm -rf {} \; 2>/dev/null
    "$(command -v sudo 2>/dev/null)" find "${pytest_root_dir}" -name .pytest_cache -type d -exec rm -rf {} \; 2>/dev/null
}


function install_clean_virtual_environment {
  cd ~ || exit
  sudo rm -rf  ~/venv
  sudo virtualenv venv
  cd "${pytest_root_dir}" || exit
}


function install_package_in_a_loop {
    while true; do
        clr_green "*** Setup.py Install *************************************************************************"
        install_clean_virtual_environment
        sudo ~/venv/bin/python3 "${pytest_root_dir}/setup.py" install

        clr_green "*** pip install -r requirements.txt **********************************************************"
        install_clean_virtual_environment
        sudo ~/venv/bin/python3 -m pip install -r "${pytest_root_dir}/requirements.txt"

        sleep "${sleeptime_on_error}"
    done
}


clean_caches "${pytest_root_dir}"
install_package_in_a_loop
