#!/bin/zsh
app_name='createFolders'

pushd ./create_folders
#~/bin/develtools/nbconvert createFolders.ipynb
jupyter-nbconvert --to python --template python_clean createFolders.ipynb
pipenv run pyinstaller --onefile --noconfirm --clean --add-data Help.md:. --add-data logging_cfg.ini:. --add-data createFolders.ini:. --exclude-module IPython $app_name.py
#pipenv run pyinstaller $app_name.spec --noconfir --clean
#pushd ./dist
#tar cvzf  ../../$app_name.tgz ./$app_name
#popd
popd
~/bin/develtools/pycodesign.py codesign.ini
