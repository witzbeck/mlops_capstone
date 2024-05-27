#!/bin/bash

# Define the directories of the child packages
child_packages=("app" "frontend")

# Script to lock only if pyproject.toml has changed
for package in "${child_packages[@]}"; do
    echo "Updating lock file in $package"
    cd "$package"
    poetry lock --no-update
    cd ..
done
