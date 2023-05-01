#!/bin/sh

set -e
trap 'kill $PID' EXIT

./run.sh &
PID=$!

sleep 3

newman run forum_test_collection.postman_collection.json -e env_test.json

kill $PID