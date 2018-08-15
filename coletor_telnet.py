from pathlib import Path
from threading import Thread
import telnetlib
import os

def writing_bills(dir, telnet):
    while True:
        if Path(('{}{}billing.txt'.format(curr_dir,os.sep))).is_file():
            file = open('{}{}billing.txt'.format(curr_dir,os.sep),mode='a+')
        else:
            file = open('{}{}billing.txt'.format(curr_dir,os.sep),mode='w+')
        bill = telnet.read_until('\n\r'.encode('utf-8')).decode('utf-8')
        file.writelines(bill)
        file.close()
        print('Escrevendo o bilhete {}'.format(bill))

print ('''
888888888888         88
     88              88                             ,d
     88              88                             88
     88   ,adPPYba,  88  8b,dPPYba,    ,adPPYba,  MM88MMM
     88  a8P_____88  88  88P'   `"8a  a8P_____88    88
     88  8PP"""""""  88  88       88  8PP"""""""    88
     88  "8b,   ,aa  88  88       88  "8b,   ,aa    88,
     88   `"Ybbd8"'  88  88       88   `"Ybbd8"'    "Y888
''')

host = input('Digite o endereço IP do Host => ')

try:
    port = int(input('Digite a porta do Host => '))
except:
    print('São permitidos somente números inteiros!')
    exit(0)

print('Tentando conectar-se ao {}:{}'.format(host,port))

try:
    telnet = telnetlib.Telnet(host, port, 20)
except Exception as e:
    print('Não foi possível conectar-se ao {}:{}'.format(host,port))
    print('Exceção: {}'.format(e))
    exit(0)

telnet.open

curr_dir = os.getcwd()

t = Thread(target=writing_bills, args=(curr_dir,telnet,))
t.start()
