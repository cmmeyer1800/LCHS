WD=$(pwd)

PATH="${WD}/settings.json"

export SETTINGSPATH="${PATH}"
export FLASK_APP=lchs

python3 -m flask run --port=5000 --host="0.0.0.0"