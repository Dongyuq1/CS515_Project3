#!/bin/sh

if ! pip3 install flask; then
    echo "Failed to install Flask"
    exit 1
fi

if ! npm install -g newman; then
    echo "Failed to install Newman"
    exit 1
fi
