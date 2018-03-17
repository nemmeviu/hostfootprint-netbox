#!/bin/bash

help(){
    echo "usage: $0 host indice tipo"
    echo
    exit 0
}

[ -z $1 ] && help;
[ -z $2 ] && help;
[ -z $3 ] && help;

HOST=$1
INDICE=$2
TIPO=$3

curl -H 'Content-Type: application/json' -XDELETE http://"$HOST":9200/"$INDICE"/?pretty
curl -H 'Content-Type: application/json' -XPUT http://"$HOST":9200/"$INDICE"/?pretty
curl -H 'Content-Type: application/json' -XPUT http://"$HOST":9200/"$INDICE"/_mapping/"$TIPO"?pretty --data-binary @"$INDICE"/"$TIPO"/mapping.json
