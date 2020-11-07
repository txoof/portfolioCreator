#!/bin/zsh
source_path=./create_folders

#publish_tar=createFolders.tgz
publish_pkg=createfolders.pkg

version_number=`grep version $source_path/constants.py | sed -nE  's/^version[ ]+=[ ]+(.*)/\1/p' | tr -d \'\"`


if [ -z "$1" ]; then
  echo current version number: v$version_number
  echo tar build, tag and push release to github
  echo usage:
  echo $0 \"release comment\"
  exit 0
fi

tag="v$version_number"

git tag -a "$tag" -m "$1"
git commit -m "update pkg distribution $1" $publish_pkg
git push origin $tag 
