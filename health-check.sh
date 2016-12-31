#!/bin/bash

if [ $# != 3 ]; then
    echo "Usage: $0 <stack> <appname> <env>"
    echo "Examples:\n $0 lilly lilly-api ci\n"
    exit 1
fi

curl -s $1-$2-svc.$1-$3.svc.walkure.net | grep Hello
