git config --global --add safe.directory ${containerWorkspaceFolder}

pip3 install --user -r requirements.txt

poetry config virtualenvs.in-project true

poetry install
poetry shell
