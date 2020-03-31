#!/usr/bin/env bash
export FLASK_ENV=development
export FLASK_APP=app/main.py
# root dir
export FS_ROOT_DIR=$1
flask run
