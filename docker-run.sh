#!/usr/bin/env bash
app="filesystem-app-wg"
export FS_ROOT_DIR=$1
docker run -d -p 8080:80 --name=${app} ${app}
