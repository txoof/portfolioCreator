#!/bin/zsh
source_path=./create_folders
publish_tar=portfolioCreator.tgz

if [ -z "$1" ]; then
  echo Build a pyinstaller, tar build, tag and push release to github
  echo usage:
  echo $0 "release comment"
  exit 0
fi

# run the build script
./build.sh

version_number=`grep version $source_path/constants.py | sed -nE  's/^version[ ]+=[ ]+(.*)/\1/p' | tr -d \'\"`

tag = "v$version_number"

git tag $tag
git commit -m "update tar distribution $1" $publish_tar
git push origin $tag $1
