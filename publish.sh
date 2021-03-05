#!/bin/zsh
source_path=./create_folders

#publish_tar=insert_files.tgz
publish_pkg=createfolders.pkg

version_number=$(grep version $source_path/constants.py | sed -nE  's/^version[ ]+=[ ]+(.*)/\1/p' | tr -d \'\")



if [ -z "$1" ]; then
  echo $0 updates the readme with current version number and pushes
  echo and tags a release of $publish_pkg to github
  echo " " 
  echo current version number: v$version_number
  echo tar build, tag and push release to github
  echo usage:
  echo $0 \"release comment\"
  exit 0
fi

echo "updating README.md"

if ! command -v /usr/local/bin/gsed
then
  echo "gnu-sed must be installed for this script to function properly:"
  echo "$ brew install gnu-sed"
  exit 1
else
  gsed -i "s/\(## Current Version:\).*/\1 $version_number/g" README.md
  gsed -i "s/^M//g" README.md
  git commit -m "update version " README.md
fi

tag="v$version_number"

pycodesign.py -O $version_number codesign.ini

if [ $? -ne 0 ] 
then
  echo codesigning failed, exiting
  exit 1
fi

git tag -a "$tag" -m "$1"
git commit -m "update tar distribution $1" $publish_pkg
git push origin $tag 
