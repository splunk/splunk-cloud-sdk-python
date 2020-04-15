#!/usr/bin/env bash

rm -rf docs
mkdir -p docs

pdoc --output-dir docs splunk_sdk

cd docs/splunk_sdk

DOC_INDEX="

#  github.com/splunk/splunk-cloud-sdk-python

## Packages

"

# generate md for directory modules under splunk_sdk
for module in $(ls); do
  for spec_version in $(ls $module); do
    if [[ "$spec_version" == "index.md" ]]; then
      continue
    fi

    for file_name in $(ls $module/$spec_version); do
      if [[ "$file_name" == "index.md" ]]; then
        continue
      fi
      DOC_INDEX+="* [$module/$spec_version/$file_name](splunk_sdk/$module/$spec_version/$file_name)
"
    done
  done
done

echo "$DOC_INDEX" >../../docs/README.md
