
try:
    import requests
except Exception as e:
    print('>>> Biblioteca requests não encontrada instalar utilizando => pip install requests')
    exit(1)

try:
    from bs4 import BeautifulSoup
except Exception as e:
    print('>>> Biblioteca BeautifulSoup não encontrada instalar utilizando => pip install bs4')
    exit(1)

import argparse
import datetime
import time
import re
import sys

def monta_req_files(vonixHtml, fila, troncos_qtd, period_begin, period_end):
    return [
        ('authenticity_token', (None, vonixHtml.findAll('meta')[2]['content'])),
        ('queue[name]', (None, fila.title())),
        ('queue[description]', (None, fila.title())),
        ('queue[image_type]', (None, 'N')),
        ('queue[image_number]', (None, '8')),
        ('queue[image_file]; filename=', (None, '', 'application/octe-stream')),
        ('queue[is_in]', (None, '0')),
        ('queue[is_in]', (None, '1')),
        ('queue[is_out]', (None, '0')),
        ('queue[is_auto]', (None, '0')),
        ('queue[is_auto]', (None, '1')),
        ('queue_property[strategy]', (None, 'leastrecent')),
        ('queue_property[autofill]', (None, 'yes')),
        ('queue_property[MAXLEN_GROUP]', (None, 'no')),
        ('queue_property[joinempty]', (None, 'yes')),
        ('queue_property[leavewhenempty]', (None, 'strict')),
        ('queue_property[context]', (None, 'n')),
        ('queue_property[weight]', (None, '0')),
        ('queue_property[musicclass]', (None, 'default')),
        ('queue_property[ANNOUNCE_FREQUENCY_GROUP]', (None, 'no')),
        ('queue_property[PERIODIC_ANNOUNCE_GROUP]', (None, 'yes')),
        ('queue_property[periodic-announce-frequency]', (None, '')),
        ('queue_property[OFFER_MODE]', (None, 'auto')),
        ('queue_property[retry]', (None, '1')),
        ('queue_property[memberdelay]', (None, '0')),
        ('queue_property[wrapuptime]', (None, '10')),
        ('queue_property[autopause]', (None, 'yes')),
        ('queue_property[ANNOUNCE_GROUP]', (None, 'receptivo')),
        ('queue[ivr_message]', (None, '')),
        ('queue[ivr_message_frequency]', (None, 'always')),
        ('queue[ivr_message_reps]', (None, '')),
        ('queue[ivr_message_interval]', (None, '')),
        ('queue[sla_percent]', (None, '90')),
        ('queue[sla_secs]', (None, '60')),
        ('queue[callerid]', (None, '00000000')),
        ('queue[show_callerid]', (None, 'allowed')),
        ('queue[lcr_profile_id]', (None, '1')),
        ('queue[max_call_secs]', (None, '0')),
        ('queue[id]', (None, fila.lower())),
        ('dialer[max_trunks]', (None, troncos_qtd)),
        ('dialer[mode]', (None, 'SimpleDial')),
        ('dialer[dial_speed]', (None, '1')),
        ('dialer[timeout]', (None, '15')),
        ('dialer[period][weekday][]', (None, '1')),
        ('dialer[period][period_begin][]', (None, period_begin)),
        ('dialer[period][period_end][]', (None, period_end)),
        ('dialer[period][weekday][]', (None, '2')),
        ('dialer[period][period_begin][]', (None, period_begin)),
        ('dialer[period][period_end][]', (None, period_end)),
        ('dialer[period][weekday][]', (None, '3')),
        ('dialer[period][period_begin][]', (None, period_begin)),
        ('dialer[period][period_end][]', (None, period_end)),
        ('dialer[period][weekday][]', (None, '4')),
        ('dialer[period][period_begin][]', (None, period_begin)),
        ('dialer[period][period_end][]', (None, period_end)),
        ('dialer[period][weekday][]', (None, '5')),
        ('dialer[period][period_begin][]', (None, period_begin)),
        ('dialer[period][period_end][]', (None, period_end)),
        ('queue[call_duration_alarm]', (None, '0')),
        ('queue[wait_duration_alarm]', (None, '0')),
        ('has_alarm_idle_duration', (None, '1')),
        ('queue[idle_duration_alarm]', (None, '60')),
        ('queue[id]', (None, fila.lower())),
        ('x', (None, '21')),
        ('y', (None, '12'))]

def check_ip(ip):
    regex = re.compile('^((10)|(172)|(192)){1}\.([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])$')
    if not regex.match(ip):
        raise argparse.ArgumentTypeError('O IP {} é inválido!'.format(ip))
    return ip

BANNER ='''
      _ _       _ _                       _  _           _            _
   __| (_) __ _| | | ___ _ __    __ _  __| |(_)_   _ ___| |_ ___ _ __| |
  / _` | |/ _` | | |/ _ \ '__|  / _` |/ _` || | | | / __| __/ _ \ '__| |
 | (_| | | (_| | | |  __/ |    | (_| | (_| || | |_| \__ \ ||  __/ |  |_|
  \__,_|_|\__,_|_|_|\___|_|     \__,_|\__,_|/ |\__,_|___/\__\___|_|  (_)
                                          |__/                          '''

#Checar os argumentos
print(BANNER)
parser = argparse.ArgumentParser(prog='dialler_adjuster')
parser.add_argument('--ip', help='Endereço IP do discador.', required=True, type=check_ip)
parser.add_argument('--username', help='Nome do usuário Adm. do discador.', required=True)
parser.add_argument('--password', help='Senha do usuário Adm. do discador.', required=True)
parser.add_argument('--queues', help='Nome do arquivo parametros das filas discador.', required=True, type=argparse.FileType('r'))
parser.add_argument('--trunks_add', help='Quantidade de troncos a aumentar', default=3, type=int)
parser.add_argument('--trunks_max', help='Quantidade máxima de troncos do discador.', default=60, type=int)

args = parser.parse_args()

#Dados do discador
url_login   = 'http://{}/login/signin'.format(args.ip)
url_adm     = 'http://{}/admin/queue_save'.format(args.ip)
url_index   = 'http://{}'.format(args.ip)
url_sip     = 'http://{}/admin/extension_list'.format(args.ip)
filas       = {'id':[]}

#Le o arquivo Layout NOME_DA_FILA;HORA_INICIAL;HORA_FINAL
with args.queues as queues:
    for lines in queues:
        filas['id'].append({'fila':'{}'.format(lines.split(';')[0]), 'period':['{}'.format(lines.split(';')[1]),'{}'.format(lines.split(';')[2].rstrip('\n\r'))]})

while(True):
    with requests.Session() as s:
        #Loop nas filas
        for fila in filas['id']:
            #Faz o login na página inicial
            try:
                r = s.post(url_login, data={'authenticity_token': BeautifulSoup(s.get(url_login).text, 'html.parser').input['value'],'return_to':'','username':'{}'.format(args.username),'password':'{}'.format(args.password),'commit':'Entrar'}, cookies={'queue':fila['fila']}, timeout=20)
            except Exception as e:
                print('***ERRO REQUISIÇÃO POST!\n{}'.format(e))
                continue

            #Faz a requisição GET para capturar os Status das operadoras SIP
            try:
                vonixHtml = BeautifulSoup(s.get(url_sip, timeout=20).text, 'html.parser').findAll(id=re.compile('^(extension_)[a-zA-Z]{1,}$'))
                print('\tRAMAL\tIP\t\tPORTA\t\tLATENCIA\t\tSTATUS')
                for sip in vonixHtml:
                    for op in sip.get_text().lstrip('\n').split('\n'):
                        if op in ('-','\n'):
                            continue
                        print('{:>9}\t'.format(op), end='')
                    print()
                time.sleep(3)
            except Exception as e:
                print('***ERRO REQUISIÇÃO POST!\n{}'.format(e))

            #Caso fila estiver fora de horário pula
            if datetime.datetime.time(datetime.datetime.now()).hour < int(fila['period'][0]) or datetime.datetime.time(datetime.datetime.now()).hour > int(fila['period'][1]):
                print('\n***ATENÇÃO FILA {} FORA DE HORÁRIO => {}:{}'.format(fila['fila'], fila['period'][0], fila['period'][1]))
                continue

            vonixHtml   = BeautifulSoup(r.text, 'html.parser')

            #Caso fila esteja sem contatos gera um alerta e zera os troncos
            if vonixHtml.find(id='{}_stat_status'.format(fila['fila'])).get_text().upper() == 'SEM CONTATOS':
                r = s.post(url_adm, files=monta_req_files(vonixHtml, fila['fila'], 0, fila['period'][0], fila['period'][1]), timeout=20)
                print('\n***ATENÇÃO FILA {} SEM CONTATOS!\n***DIMINUI QUANTIDADE DE TRONCOS PARA => 0!'.format(fila['fila']))
                continue

            abandonadas = int(vonixHtml.find(id='auto_abandoned').get_text())
            trunks_max  = int(vonixHtml.find(id='{}_stat_trunks'.format(fila['fila'])).get_text().split('/')[1])
            trunks_min  = int(vonixHtml.find(id='{}_stat_trunks'.format(fila['fila'])).get_text().split('/')[0])

            #Caso diferença de Troncos Máximo com a Mínima for maior que 9 setar quantidade mínima
            if (trunks_max - trunks_min) > 9:
                r = s.post(url_adm, files=monta_req_files(vonixHtml, fila['fila'], 2 if trunks_min < 0 else trunks_min + 2, fila['period'][0], fila['period'][1]), timeout=20)
                print('***DIMINUI QUANTIDADE DE TRONCOS DE => {} PARA => {}!\n'.format(trunks_max, 2 if trunks_min < 0 else trunks_min + 2))
                continue

            fila_espera = int(vonixHtml.find(id='auto_waiting').get_text())
            #Caso já tenha uma chamada em espera, aguardar 3 segundos e capturar novamente
            if fila_espera > 0:
                r = s.post(url_adm, files=monta_req_files(vonixHtml, fila['fila'], 2 if (trunks_max - fila_espera) < 0 else (trunks_max - fila_espera), fila['period'][0], fila['period'][1]), timeout=20)
                print('***CHAMADA EM ESPERA => {} DIMINUI QUANTIDADE DE TRONCOS DE => {} PARA => {}!\n'.format(fila_espera, trunks_max, 2 if (trunks_max - fila_espera) < 0 else (trunks_max - fila_espera)))
                time.sleep(5)
                continue

            print(BANNER)
            print('***STATUS***\n***FILA ATUAL => {}\n***CHAMADAS ABANDONADAS => {} TRONCOS => {}!\n'.format(fila['fila'], abandonadas, trunks_max))
            qtd_troncos = 0
            regex_idle  = re.compile('^'+fila['fila']+'_[0-9]{1,4}_idle_time$')
            for idle in vonixHtml.findAll(id=regex_idle):
                print('>>>AGENTE => {} OCIOSIDADE => {} STATUS => {}...'.format(vonixHtml.find(id='{}_{}'.format(fila['fila'], idle['id'].split('_')[1])).get_text().lstrip('\n').split('\n')[0].rstrip(), idle.get_text(), vonixHtml.findAll(id=idle['id'].replace('idle_time', 'status'))[0].get_text().upper().strip()))
                if idle.get_text() == '-':
                    continue

                if 'm' not in idle.get_text():
                    duration = int(idle.get_text().replace(' ', '').split('s')[0])
                else:
                    duration = (int(idle.get_text().replace(' ', '').split('m')[0]) * 60) + int(re.sub(r'^[0-9]{1,2}(m).', '', idle.get_text()).rstrip('s'))

                if duration <= 20:
                    continue

                if not vonixHtml.findAll(id=idle['id'].replace('idle_time', 'status'))[0].get_text().upper().strip() == 'DISPONIVEL':
                    continue

                fila_espera = int(BeautifulSoup(s.get(url_index, cookies={'queue':fila['fila']}).text, 'html.parser').find(id='auto_waiting').get_text())
                #Caso já tenha uma chamada em espera, aguardar 3 segundos e capturar novamente
                if fila_espera > 0:
                    r = s.post(url_adm, files=monta_req_files(vonixHtml, fila['fila'], 2 if (trunks_max - fila_espera) < 0 else (trunks_max - fila_espera), fila['period'][0], fila['period'][1]), timeout=20)
                    print('***DIMINUI QUANTIDADE DE TRONCOS DE => {} PARA => {}!\n'.format(trunks_max, 2 if (trunks_max - fila_espera) < 0 else (trunks_max - fila_espera)))
                    time.sleep(3)
                    continue

                vonixHtml01 = BeautifulSoup(s.get(url_index, cookies={'queue':fila['fila']}).text, 'html.parser')
                trunks_max  = int(vonixHtml01.find(id='{}_stat_trunks'.format(fila['fila'])).get_text().split('/')[1])
                trunks_min  = int(vonixHtml01.find(id='{}_stat_trunks'.format(fila['fila'])).get_text().split('/')[0])
                if (trunks_max - trunks_min) > 9:
                    r = s.post(url_adm, files=monta_req_files(vonixHtml, fila['fila'], 2 if trunks_min < 0 else trunks_min, fila['period'][0], fila['period'][1]), timeout=20)
                    print('***DIMINUI QUANTIDADE DE TRONCOS DE => {} PARA => {}!\n'.format(trunks_max, 2 if trunks_min < 0 else trunks_min))
                    time.sleep(3)
                    break

                if trunks_max >= args.trunks_max:
                    print('>>>QUANTIDADE MÁXIMA DE TRONCOS ATINGIDA => {}!\n'.format(trunks_max))
                    time.sleep(3)
                    continue

                if duration <= 60:
                    qtd_troncos+= args.trunks_add
                else:
                    qtd_troncos+= (duration // 60) * args.trunks_add

            if qtd_troncos > 0 and trunks_max < args.trunks_max:
                try:
                    r = s.post(url_adm, files=monta_req_files(vonixHtml, fila['fila'], trunks_max + qtd_troncos, fila['period'][0], fila['period'][1]), timeout=20)
                    print('***AUMENTOU QUANTIDADE DE TRONCOS DE => {} PARA => {}!\n'.format(trunks_max, trunks_max + qtd_troncos))
                    print('>>>TEMPO ESPERA => {}s. ÍNICIO => {}'.format(qtd_troncos * 2, time.ctime()))
                    time.sleep(qtd_troncos * 2)
                    print('>>>FIM TEMPO ESPERA => {}'.format(time.ctime()))
                    break
                except Exception as e:
                    print('***ERRO REQUISIÇÃO POST!\n{}'.format(e))
                    continue
    s.close()
