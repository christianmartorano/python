import re
import requests
from bs4 import BeautifulSoup

url = 'http://empregacampinas.com.br/?s='

emprego = input('>>>Digite a vaga que deseja consulta => ')

try:
    r = requests.get('{}{}'.format(url, emprego), timeout=30)
except Exception as e:
    print('>>>Erro na requisição GET!\n{}'.format(e))
    exit(0)

html = BeautifulSoup(r.text, 'html.parser')

if html.find('h3').get_text().upper() == 'OPS. NADA ENCONTRADO!':
    print('>>>Não foram encontradas vagas para a pequisa => {}'.format(emprego))
    exit(0)


ultima = html.find('a', attrs={'class':'last'})['href']

paginas = input('>>>Foram encontradas {} páginas de resultado deseja capturar até a página => '.format(ultima.lstrip('http://').split('/')[2]))

if not paginas.isnumeric():
    print('>>>São aceitos somente números => {}!'.format(paginas))
    exit(0)

if int(paginas) <=0 or int(paginas) > int(ultima.lstrip('http://').split('/')[2]):
    print('>>>Valor digitado é inválido => {}!'.format(paginas))
    exit(0)

url = 'http://empregacampinas.com.br'

for p in range(int(paginas)):
    try:
        r = requests.get('{}/page/{}/?s={}'.format(url, p, emprego), timeout=30)
    except Exception as e:
        print('>>>Erro na requisição GET URL => {}!\n{}'.format(r.url, e))
        continue
    
    html = BeautifulSoup(r.text, 'html.parser')

    for h in html.findAll('a', attrs={'class':'thumbnail','href':re.compile('(http://empregacampinas.com.br).')}):
        try:
            r = requests.get(h['href'], timeout=30)
        except Exception as e:
            print('>>>Erro na requisição GET URL => {}!\n{}'.format(r.url, e))
            continue

        html_emprego = BeautifulSoup(r.text, 'html.parser')
        vaga = html_emprego.find('div', attrs={'class':'col-lg-8 conteudo-vaga'}).find('h1').get_text().lstrip('\r\n').strip()

        for s in html_emprego.find('div', attrs={'class':'col-lg-8 conteudo-vaga'}).findAll('p'):
            if 'SALÁRIO: ' in s.get_text().upper():
                salario = s.get_text().split(':')[1]

        for e in html_emprego.find('div', attrs={'class':'col-lg-8 conteudo-vaga'}).findAll('a'):
            if 'mailto:' in e['href']:
                email = e.get_text()
                break

        print('\nVAGA {}\nSALÁRIO {}\nE-MAIL {}\n'.format(vaga, salario, email))
