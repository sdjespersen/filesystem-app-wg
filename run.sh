#!/bin/bash
app="filesystem-app-wg"
docker build -t ${app} .
docker run -d -p 8080:80 --name=${app} ${app}
