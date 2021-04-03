#!/usr/bin/env bash
echo "baixando os arquivos"
pgfn_cod=`curl --request GET -sL --url 'http://localhost:8663/download/pgfn'| cut -c 17-52`
echo "preparando os arquivos"
pgfn_pre=`curl --request GET -sL --url "http://localhost:8663/prepare/pgfn/$pgfn_cod"`
echo "salvando na Amazon"
pgfn_amazon=`curl --request GET -sL --url "http://localhost:8663/send/pgfn/$pgfn_pre"`