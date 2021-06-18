#!/bin/sh

if [ -n "$SUDO_COMMAND" ]; then
    echo "Please don't run this script with sudo."
    exit
fi

red="\033[0;31m"
nocolor="\033[0m"

if ! command -v docker-compose >/dev/null; then
    echo $red "Error: docker-compose needs to be installed" $nocolor
fi

cd "$(pwd)"

if [ ! -f "$(pwd)/.env" ]; then
    mv  "$(pwd)/.env.example" "$(pwd)/.env"
fi

docker-compose build
