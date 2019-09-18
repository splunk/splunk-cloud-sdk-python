#!/usr/bin/env bash

#
#  copy_generated_files.sh <GENERATED_DIR_PATH> <TARGET_DIR_PATH>
#
#  e.g. copy_generated_files.sh <workspace>/sdk-codegen/generated/python/ <workspace>/splunk-cloud-sdk-python/splunk_sdk/

set -x

sourcedir=$1
targetdir=$2

tmpdir="/tmp/splunk_sdk"

# copy generated files to tmpdir for processing
rm -rf ${tmpdir}
mkdir -p ${tmpdir}
cd ${tmpdir}
cp -r ${sourcedir} .

# work around a problem in codegen
mv "${tmpdir}/app-registry" "${tmpdir}/app_registry"

# move files into the appropriate module
for svc in $(ls);
do
    cd ${tmpdir}/${svc}
    for ver in $(ls);
    do
        cp -r "${tmpdir}/${svc}/${ver}/splunk_sdk/${svc}/" "${tmpdir}/${svc}/${ver}/"

        # delete the redundant dir
        rm -rf "${tmpdir}/${svc}/${ver}/splunk_sdk/"

        # Note: The '(recommended version)' is declared in the comments of the __init__.py by the codegen project.
        # The version is published in the openapi spec that is maintained by each individual service team.
        # This is how the default version is determined.
        default_version=$(cat "${tmpdir}/${svc}/${ver}/__init__.py" | grep "(recommended default)")
        if [[ ! -z "${default_version}" ]]; then

          # set the recommend version
            cp "${tmpdir}/${svc}/${ver}/__init__.py"  "${tmpdir}/${svc}/"
        fi
    done
done

# copy generated files to target directory
cp -r ${tmpdir}/ ${targetdir}