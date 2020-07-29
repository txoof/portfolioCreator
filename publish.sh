#!/bin/zsh
source_path=./create_folders

# run the build script
./build.sh

version_number=`grep version $source_path/constants.py | sed -nE  's/^version[ ]+=[ ]+(.*)/\1/p' | tr -d \'\"`

git tag $version_number
git commit -m "update tar distribution"

git push
