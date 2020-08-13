#!/bin/zsh
app_name='createFolders'

pushd ./create_folders
pipenv run pyinstaller $app_name.spec --noconfir --clean
pushd ./dist
tar cvzf  ../../$app_name.tgz ./$app_name
popd
popd
