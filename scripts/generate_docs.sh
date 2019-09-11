#!/usr/bin/env bash

cd "$(dirname "$0")/../splunk_sdk"

rm -rf ../docs/pkg
rm ../docs/README.md
rm ../docs/package.json
mkdir -p ../docs/pkg

DOC_INDEX="

#  github.com/splunk/splunk-cloud-sdk-python

## Packages

"

# generate md for directory modules under splunk_sdk
for module in $(ls);
do
    # ignore files/dirs that start with _ or end with .py
    if [[ ! "$module" == _* ]] && [[ ! "$module" == *.py ]]; then
        docmd "splunk_sdk.$module" > "../docs/pkg/$module.md"
        DOC_INDEX+="* [$module](pkg/$module.md)
"
    fi
done

echo "$DOC_INDEX" > ../docs/README.md