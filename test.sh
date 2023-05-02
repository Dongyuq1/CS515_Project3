#!/bin/sh

set -e
trap 'kill $PID' EXIT

./run.sh &
PID=$!

sleep 3

newman run WebForumTestCollection.postman_collection.json -e WebForumTestEnv.postman_environment.json

kill $PID