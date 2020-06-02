#!/usr/bin/env python3
#
# Autor: Danielle dos Reis
# Date: 28/04/2020
# Version: v1

import json, sys
from datetime import datetime
from pathlib import Path

funcao = sys.argv[1]
nomeCliente = sys.argv[2]
ipCliente = sys.argv[3]

def discovery_certificado(nomeCliente, ipCliente):
    result_json = []
    data_modificacao = lambda f: f.stat().st_mtime
    diretorio = Path('/mnt/bigip-cert/check_certificado/')
    files = diretorio.glob('*')
    sorted_files = sorted(files, key=data_modificacao, reverse=True)
    arquivo = sorted_files[0]

    with open(arquivo, 'r') as file:
        lista = file.readlines()
        for linha in lista:
            dicionario = linha.replace("'", "\"")
            dicionario = json.loads(dicionario)
            lista = {'{#CLIENT}': dicionario['client'],
                     '{#IP}': dicionario['ip'],
                     '{#HOSTNAME}': dicionario['hostname'],
                     '{#NOMECERT}': dicionario['nomecert'],
                     '{#EXPIRATION}': int(datetime.strptime(dicionario['expiration'][:19], '%Y-%m-%d %H:%M:%S').timestamp())}
            if nomeCliente in lista.values() and ipCliente in lista.values():
                result_json.append(lista)

    return json.dumps({'data': result_json}, indent=4)

def expirationCertificado(nomeCliente, ipCliente, nomeCert):
    lista = discovery_certificado(nomeCliente, ipCliente)
    d1_json = json.loads(lista)
    for i in d1_json['data']:
        if nomeCert in i.values() and ipCliente in i.values():
            expiracao = i['{#EXPIRATION}']
            return int(expiracao)

if funcao == 'discovery_certificado':
    print(discovery_certificado(nomeCliente, ipCliente))
elif funcao == 'expirationCertificado':
    nomeCert = sys.argv[4]
    print(expirationCertificado(nomeCliente, ipCliente, nomeCert))
