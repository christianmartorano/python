#I did this script to automate my daily routine...
#I hope it helps someone other than me :D
#I removed the urls and data from the post due to privacy, I am available for any questions

try:
    import requests
except Exception as e:
    print('The lib requests is not installed -> pip install requests')
    exit(1)
try:
    from pathlib import Path
except Exception as e:
    print('The lib pathlib is not installed -> pip install pathlib')
    exit(1)
try:
    from dateutil.parser import parse
except Exception as e:
    print('The lib dateutil is not installed -> pip install python-dateutil')
    exit(1)

try:
    from money_parser import price_str
except Exception as e:
    print('The lib money-parser is not installed -> pip install money-parser')
    exit(1)

try:
    from bs4 import BeautifulSoup
except Exception as e:
    print('The lib BeautifulSoup is not installed -> pip install bs4')
    exit(1)

import asyncio
import datetime
import subprocess
import time
import os

#Retirar Warning https
requests.packages.urllib3.disable_warnings()

BANNER = '''

***SIT AND RELAX***

___    A
| |   {*}
| |  __V__
|_|o_|%%%|0_
   |       |
   |       |
   |_______|'''

MENU = '''

1 -> SIG
2 -> PLAN PAG
3 -> VIRTUA UPDATE
4 -> ALL
5 -> FINISH THE SCRIPT

'''

GOODBYE = '''

***BYE BYE***

.~~~~.
i====i_
|cccc|_)
|cccc|   hjw
`-==-' '''

HEADER = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

def menu_principal():
    while True:
        print(BANNER)
        print(MENU)
        option = input('Select the option => ')
        if not option.isnumeric() or int(option) > 5 or int(option) < 1:
            print('Error option not found!')
            continue
        if int(option)   == 1:
            sig()            
        elif int(option) == 2:
            asyncio.run(pag(False))            
        elif int(option) == 3:
            virtua()            
        elif int(option) == 4:
            sig()
            asyncio.run(pag(True))
            virtua()            
        else:
            print(GOODBYE)
            exit(0)
        subprocess.Popen('explorer {}'.format(TEMP), shell=True) 
        
def sig():
    for g in range(1,3):
        if not os.path.isdir('{}{}G{}'.format(TEMP, os.sep, g)):
            try:
                os.makedirs('{}{}G{}'.format(TEMP, os.sep, g))
            except Exception as e:
                print('The application throws Exception\n{}'.format(e))
                menu_principal()

    url = ''

    grupos = []
    arquivos = []

    grupos.append('G1')
    grupos.append('G2')
    arquivos.append('cadas.zip')
    arquivos.append('oper.zip')
    arquivos.append('telef.zip')
    arquivos.append('inadimp.zip')
    arquivos.append('coob.zip')
    arquivos.append('clientes-nao-contatados.csv')
    arquivos.append('clientes-potenciais.csv')
    arquivos.append('operacoes-scpc.csv')

    for g in grupos:
        #Caminha até o diretório
        os.chdir('{}{}{}'.format(TEMP, os.sep, g))

        #Limpa o diretório
        subprocess.Popen('del *.* /q', shell=True)

        for a in arquivos:
            print('Download Started => {}-{} At {}'.format(g, a, time.ctime()))
            try:
                r = requests.get('{}-{}-{}'.format(url, g, a), headers=HEADER, timeout=10, verify=False)
            except Exception as e:
                print('Timeout reached!{}'.format(e))
                print('Download Failed => {}-{} At {}'.format(g, a, time.ctime()))
                continue

            if r.headers['Content-type'].split(';')[0] == 'text/html':
                print('Download Failed => {}-{} At {}'.format(g, a, time.ctime()))
            else:
                file_download = open('{}{}{}{}{}'.format(TEMP, os.sep, g, os.sep, r.url.split('nome=')[1]), 'wb').write(r.content)
                print('Download Finished => {}-{} At {}'.format(g, a, time.ctime()))

        #Extrai os arquivos
        subprocess.Popen('7zg e *.zip', shell=True)
        time.sleep(10)

        #Deleta os arquivos zipados
        subprocess.Popen('del *.zip', shell=True)
        time.sleep(5)

        #Renomear os arquivos padrão Virtua
        for f in os.listdir():
            if f.endswith('.txt'):
                print('Renaming archive {} in {}{}_{}'.format(f, f.split('_')[2][:5].rstrip('.'), datetime.datetime.now().strftime('%Y%m%d'), g))
                os.rename(f, '{}{}_{}.txt'.format(f.split('_')[2][:5].rstrip('.'), datetime.datetime.now().strftime('%Y%m%d'), g))


async def pag(auto):
    #Caminha até o diretório
    os.chdir('{}{}'.format(TEMP, os.sep))

    for f in os.listdir('{}{}'.format(TEMP, os.sep)):
        if f.endswith('.csv'):
            #Limpa o diretório
            subprocess.Popen('del *.csv /q', shell=True)
            break

    async def do_request(session_rico, url):
        data = {}
        resp = []
        for v in (BeautifulSoup(session_rico.post(url, headers=HEADER, data=data, timeout=20).text, 'html.parser').findAll('b')):
            if not v.get_text().strip() == '':
                try:
                    resp.append(price_str(v.get_text().strip()))
                except Exception as e:
                    continue
        return resp
    def download_plan(session_rico, data_ini, data_fim, grupo):
        url = 'data_de={}&data_ate={}'.format(data_ini.strftime('%d/%m/%Y'), data_fim.strftime('%d/%m/%Y'))
        try:
            r = session_rico.get(url, headers=HEADER, timeout=10)
        except Exception as e:
            print('Timeout reached!{}'.format(e))
            return False

        if r.headers['Content-type'].split(';')[0] == 'text/html':
            print('Download Failed => {} At {}'.format(url, time.ctime()))
            return False
        else:
            file_download = open('{}{}plan{}_{}.csv'.format(TEMP, os.sep, datetime.datetime.now().strftime('%Y%m%d'), grupo), 'wb').write(r.content)
            print('Download Finished => {} At {}'.format(url, time.ctime()))
            return True


    while True:
        with requests.Session() as s:
            url = ['',
                   '',
                   '']
            try:
                r = s.get(url[0], headers=HEADER, timeout=10)
            except Exception as e:
                print('Timeout reached!{}'.format(e))
                menu_principal()

            usuario = input('Enter user => ').lower()
            senha   = input('Enter password => ')

            while True:
                grupo   = input('Enter group G1 or G2 => ').upper()
                if not grupo in ('G1','G2'):
                    print('Enter the correct group {}!'.format(grupo))
                else:
                    break

            data    = {''}
            try:
                r = s.post(url[1], headers=HEADER, data=data, timeout=10)
            except Exception as e:
                print('Timeout reached!{}'.format(e))
                menu_principal()

            rico = BeautifulSoup(r.text, 'html.parser')

            if len(rico.findAll('b')) > 0:
                if 'Usuário ou senha inválidos' in rico.findAll('b')[3]:
                    print(rico.findAll('b')[3])
                    continue

            while True:
                data_ini = input('Please enter report start date (DD.MM.YYYY) => ')
                try:
                    data_ini = parse(data_ini)
                except Exception as e:
                    print(str(e).capitalize())
                    continue
                if datetime.datetime.date(data_ini) >= datetime.datetime.date(datetime.datetime.now()):
                    print('The start date can not be greater than or equal today\'s date {:%d/%m/%Y}'.format(datetime.datetime.now()))
                    continue
                break

            while True:
                data_fim = input('Please enter report end date (DD.MM.YYYY) => ')
                try:
                    data_fim = parse(data_fim)
                except Exception as e:
                    print(str(e).capitalize())
                    continue
                if data_fim < data_ini:
                    print('The end date can not be less than start date {:%d/%m/%Y}'.format(data_fim))
                    continue
                break

            rico = await asyncio.create_task(do_request(s, url[2]))

            print('Amount paid {}\t Fine value {}\t Net value {}\t Amount amortized {}\t Interest rate {}\t Remuneration {}'.format(rico[0], rico[1], rico[2], rico[3], rico[4], rico[5]))
            while True:
                option = input('Download the report(Y/N) => ').upper()
                if option == 'Y':
                    ret = download_plan(s, data_ini, data_fim, grupo)
                elif option == 'N':
                    menu_principal()
                else:
                    print('Option not found {}!'.format(option))
                    continue
                break
            option = input('Download another group report(Y/Other char) => ').upper()
            if not option == 'Y' and auto == False:
                menu_principal()
            elif option == 'Y':
                continue
            else:
                break


def virtua():
    #Caminha até o diretório
    os.chdir('{}{}'.format(TEMP, os.sep))

    for f in os.listdir('{}{}'.format(TEMP, os.sep)):
        if f.endswith('.exe'):
            #Limpa o diretório
            subprocess.Popen('del *.exe /q', shell=True)
            break

    url = ['http://www.virtuasoftware.com.br/conteudo.php?content=downloads&lang=pt-br',
           'http://www.virtuasoftware.com.br{}']

    try:
        r = requests.get(url[0], headers=HEADER, timeout=10)
    except Exception as e:
        print('Timeout reached!{}'.format(e))
        menu_principal()

    try:
        virtua_vSite = BeautifulSoup(r.text, 'html.parser').findAll('a')[11]['href'].split('//')[1]
    except Exception as e:
        print('Error {}'.format(e))
        menu_principal()

    while True:
        option = input('Version found {}. You wish download it(Y/N) => '.format(virtua_vSite)).upper()
        if option == 'N':
            menu_principal()
        elif option == 'Y':
            break
        else:
            print('Option not found {}!'.format(option))

    try:
        r = requests.get(url[1].format(BeautifulSoup(r.text, 'html.parser').findAll('a')[11]['href']), headers=HEADER, timeout=10)
    except Exception as e:
        print('Timeout reached!{}'.format(e))
        menu_principal()

    file_download = open('{}{}{}'.format(TEMP, os.sep, virtua_vSite), 'wb').write(r.content)
    print('Download Finished => {} At {}'.format(virtua_vSite, time.ctime()))
    menu_principal()

if __name__ == '__main__':
    TEMP = Path('C:{}Temp{}SIG'.format(os.sep, os.sep))
    if not os.path.isdir(TEMP):
        try:
            TEMP.mkdir()
        except Exception as e:
            print('The application throws Exception\n{}'.format(e))
            exit(1)
    menu_principal()
