#Funcionando somente a consulta a 1 telefone!

import requests
import argparse

def consulta_operadora(fone):
    url = 'http://qualoperadora.info/widget/consulta'
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    data = {'tel':'{}'.format(fone)}

    response = requests.post(url, headers=header, data=data)

    if not response.status_code == 200:
        print('Não foi possível obter a resposta! Http-Code -> {}'.format(response.status_code))
        return ''

    try:
        return response.content.decode('utf-8').split('class="o"')[1].split('title="')[1].split('"')[0]
    except:
        return 'não encontrada'

print ('''
  _____  _                         _____                      _ _
 |  __ \| |                       / ____|                    | | |
 | |__) | |__   ___  _ __   ___  | |     ___  _ __  ___ _   _| | |_
 |  ___/| '_ \ / _ \| '_ \ / _ \ | |    / _ \| '_ \/ __| | | | | __|
 | |    | | | | (_) | | | |  __/ | |___| (_) | | | \__ \ |_| | | |_
 |_|    |_| |_|\___/|_| |_|\___|  \_____\___/|_| |_|___/\__,_|_|\__|

''')

parser = argparse.ArgumentParser(description='Consultar a operadora de um telefone ou de um arquivo de telefones.', add_help=False)

parser.add_argument('--fone', metavar='NR FONE', help='O número do telefone para consulta')

parser.add_argument('--arq', metavar='FILE.TXT', help='Arquivo no formato 1 telefone por linha')

parser.add_argument('--proxy', help='Utilizar proxy para as consultas')

parser.add_argument('--qtd', metavar='N', help='Quantidade de consultas por proxy')

parser.add_argument('--random_agent', help='Utilizar User-Agents randômicos')

args = parser.parse_args()

if not args.fone and not args.arq:
    print('Informar pelo menos um telefone ou arquivo de telefones!')
    exit(0)

operadora = consulta_operadora(args.fone)

if operadora == '':
    exit(0)
else:
    print('O telefone {} pertence a operadora {}.'.format(args.fone, operadora))
