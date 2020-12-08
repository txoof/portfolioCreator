#!/bin/zsh
app_name='createFolders'
source_path=./create_folders
version_number=$(grep version $source_path/constants.py | sed -nE  's/^version[ ]+=[ ]+(.*)/\1/p' | tr -d \'\")

pushd $source_path
echo "runing nbconvert on $app_name.ipynb"
jupyter-nbconvert --to python --template python_clean $app_name.ipynb
echo "building with pyinstaller"
pipenv run pyinstaller --onefile --noconfirm --clean --add-data Help.md:. --add-data logging_cfg.ini:. --add-data createFolders.ini:. --exclude-module IPython $app_name.py
