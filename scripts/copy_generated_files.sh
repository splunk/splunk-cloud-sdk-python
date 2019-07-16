#!/usr/bin/env bash

sourcedir=$1

for dir in ${sourcedir}/*
do
    for svc in ${dir}/splunk_sdk/*
    do
        rm splunk_sdk/$(basename ${svc})/gen_*.py
        cp ${svc}/*.py splunk_sdk/$(basename ${svc})/
    done
done
