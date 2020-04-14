#!/usr/bin/env bash

rm -rf docs/pkg
mkdir -p docs/pkg

pdoc --output-dir docs/pkg splunk_sdk
