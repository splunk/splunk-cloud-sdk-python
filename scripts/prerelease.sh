#!/bin/bash -e

####################################################################################################
# Check for required env vars
####################################################################################################
if [[ "${CI}" != "true" ]] ;  then
    echo "Exiting: $0 can only be run from the CI system."
    exit 1
fi
if [[ -z "${GITLAB_HOST}" ]] ; then
    echo "GITLAB_HOST must be set, exiting ..."
    exit 1
fi
if [[ -z "${GITLAB_TOKEN}" ]] ; then
    echo "GITLAB_TOKEN must be set, exiting ..."
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

####################################################################################################
# Convert the release tag (e.g. v1.0.0) -> NEW_RELEASE (e.g. 1.0.0)
####################################################################################################
NEW_VERSION=$(echo "${CI_COMMIT_REF_NAME}" | sed "${SED_FLG}" -n 's/^v([0-9]+\.[0-9]+\.[0-9]+)$/\1/p')
if [[ -z "${NEW_VERSION}" ]] ; then
    echo "error setting NEW_VERSION, the release tag must match this pattern: \"^v([0-9]+\.[0-9]+\.[0-9]+)$\" (e.g. v1.0.0) but tag is: ${CI_COMMIT_REF_NAME} ..."
    exit 1
fi

################################################################################################################
# Checkout latest version of Gitlab code to prepare for release (Checkout develop and create new release branch)
################################################################################################################
OWNER=devplat-pr-32
PROJECT=splunk-cloud-sdk-python
BRANCH_NAME=develop
RELEASE_BRANCH_NAME=release/v${NEW_VERSION}
set +x
git remote set-url origin "https://oauth2:${GITLAB_TOKEN}@${GITLAB_HOST}/${OWNER}/${PROJECT}.git"
set -x
git config user.email "srv-dev-platform@splunk.com"
git config user.name "srv-dev-platform"
echo "Running \"git checkout ${BRANCH_NAME}\" ..."
git checkout "${BRANCH_NAME}"
echo "Running \"git fetch --all && git pull --all\" ..."
git fetch --all && git pull --all
echo "Running \"git checkout -b ${RELEASE_BRANCH_NAME}\" ..."
git checkout -b ${RELEASE_BRANCH_NAME}
echo "Showing changes with 'git status' ..."
git status

####################################################################################################
# Update splunk_sdk/__version__.py using the pre-release tag e.g. 1.0.0 for v1.0.0
####################################################################################################
echo "Updating Version in splunk_sdk/__version__.py using sed \"${SED_FLG}\" -i '' -e \"s/\\"[0-9]+\.[0-9]+\.[0-9]+\\"/\\"${NEW_VERSION}\\"/g\" splunk_sdk/__version__.py ..."
sed "${SED_FLG}" -i -e "s/\"[0-9]+\.[0-9]+\.[0-9]+\"/\"${NEW_VERSION}\"/g" splunk_sdk/__version__.py
git add splunk_sdk/__version__.py

####################################################################################################
# Append the message from the pre-release tag to the top of the CHANGELOG.md under ## Version x.y.z
####################################################################################################
echo "Adding tag message to changelog ..."
set +x
TAG_MESSAGE=$(git cat-file -p "${CI_COMMIT_REF_NAME}" | tail -n +6)
set -x
printf "Adding release notes to top of CHANGELOG.md:\n\n${TAG_MESSAGE}\n\n"
set +x
CL_HEADER=$(head -n 1 CHANGELOG.md)
CL_CONTENTS=$(tail -n +2 CHANGELOG.md)
rm CHANGELOG.md
printf "${CL_HEADER}\n\n## Version ${NEW_VERSION}\n${TAG_MESSAGE}\n${CL_CONTENTS}" > CHANGELOG.md
set -x
git add CHANGELOG.md

####################################################################################################
# Adding/pushing changed files to release branch (__version__.py and CHANGELOG.md)
####################################################################################################
echo "Showing changes with \"git status\" ..."
git status
echo "Creating commit for __version__.py and CHANGELOG.md ..."
git commit -m "Prepare v${NEW_VERSION} for release"
echo "Pushing branch ${RELEASE_BRANCH_NAME} ..."
git push --set-upstream origin "${RELEASE_BRANCH_NAME}"
