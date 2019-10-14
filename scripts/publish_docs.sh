#!/bin/bash

####################################################################################################
# Check for required env vars
####################################################################################################
if [[ "${CI}" != "true" ]] ;  then
    echo "Exiting: $0 can only be run from the CI system."
    exit 1
fi
if [[ -z "${ARTIFACT_USERNAME}" ]] ; then
    echo "ARTIFACT_USERNAME must be set, exiting ..."
    exit 1
fi
if [[ -z "${ARTIFACT_PASSWORD}" ]] ; then
    echo "ARTIFACT_PASSWORD must be set, exiting ..."
    exit 1
fi
if [[ -z "${ARTIFACTORY_NPM_REGISTRY}" ]] ; then
    echo "ARTIFACTORY_NPM_REGISTRY must be set, exiting ..."
    exit 1
fi

####################################################################################################
# Set platform-specific sed extended syntax flag
####################################################################################################
if [[ "$(uname)" == "Darwin" ]] ; then
    # MacOS
    SED_FLG="-E"
else
    # Linux
    SED_FLG="-r"
fi

# Go to project root splunk-cloud-sdk-python
cd "$(dirname "$0")/.."

####################################################################################################
# Get release version from splunk_sdk/__version__.py
####################################################################################################
NEW_VERSION=$(cat splunk_sdk/__version__.py | sed ${SED_FLG} 's/__version__ = //g' | sed 's/"//g')
if [[ -z "${NEW_VERSION}" ]] ; then
    echo "error setting NEW_VERSION from splunk_sdk/__version__.py, version must be set to match: __version__ =  \"([0-9]+\.[0-9]+\.[0-9]+.*)\" (e.g. __version__ = \"1.0.0b5\") but format found is:\n\n$(cat splunk_sdk/__version__.py)\n\n..."
    exit 1
fi

echo "Publishing docs for v${NEW_VERSION} ..."

# Run from project root
cd "scripts/"
#####################################################################################################
## Write a package.json file, this is needed by @splunk/cicd-tools even though this isn't js
#####################################################################################################
rm package.json
PACKAGE_JSON="{
    \"name\": \"@splunk/splunk-cloud-sdk-python\",
    \"version\": \"${NEW_VERSION}\",
    \"description\": \"Splunk Cloud SDK for Python\"
}"
echo ${PACKAGE_JSON} > package.json
rm -rf build/
#####################################################################################################
## Install @splunk/cicd-tools from artifactory
#####################################################################################################
npm add --no-save @splunk/cicd-tools --registry "${ARTIFACTORY_NPM_REGISTRY}"
#####################################################################################################
## Publish docs to artifactory with @splunk/cicd-tools/cicd-publish-docs
#####################################################################################################
npx cicd-publish-docs --force ../docs/
echo "Docs built and packaged into $(dirname "$0")/build"