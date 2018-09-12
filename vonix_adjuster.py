import datetime
import requests
import time
import re
from bs4 import BeautifulSoup

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

#Trocar para o endereço IP do servidor
url_login   = 'http://0.0.0.0'
url_adm     = 'http://0.0.0.0'
url_index   = 'http://0.0.0.0'
filas       = {'id':[{'fila':'XXXX','period':['X','XX']},{'fila':'XXXX','period':['XX','XX']}]}
WELCOME ='''
      _ _       _ _                       _  _           _            _
   __| (_) __ _| | | ___ _ __    __ _  __| |(_)_   _ ___| |_ ___ _ __| |
  / _` | |/ _` | | |/ _ \ '__|  / _` |/ _` || | | | / __| __/ _ \ '__| |
 | (_| | | (_| | | |  __/ |    | (_| | (_| || | |_| \__ \ ||  __/ |  |_|
  \__,_|_|\__,_|_|_|\___|_|     \__,_|\__,_|/ |\__,_|___/\__\___|_|  (_)
                                          |__/                          '''
while(True):
    with requests.Session() as s:
        #Loop nas filas
        for fila in filas['id']:
            #Caso fila estiver fora de horário pula
            if datetime.datetime.time(datetime.datetime.now()).hour < int(fila['period'][0]) or datetime.datetime.time(datetime.datetime.now()).hour > int(fila['period'][1]):
                print('\n***ATENÇÃO FILA {} FORA DE HORÁRIO => {}:{}'.format(fila['fila'], fila['period'][0], fila['period'][1]))
                continue

            #Faz o login na página inicial
            try:
                r = s.post(url_login, data={'authenticity_token': BeautifulSoup(s.get(url_login).text, 'html.parser').input['value'],'return_to':'','username':'XXXX','password':'XXXX','commit':'Entrar'}, cookies={'queue':fila['fila']}, timeout=20)
            except Exception as e:
                print('***ERRO REQUISIÇÃO POST!\n{}'.format(e))
                continue

            vonixHtml   = BeautifulSoup(r.text, 'html.parser')
            abandonadas = int(vonixHtml.find(id='auto_abandoned').get_text())
            trunks_max  = int(vonixHtml.find(id='{}_stat_trunks'.format(fila['fila'])).get_text().split('/')[1])
            trunks_min  = int(vonixHtml.find(id='{}_stat_trunks'.format(fila['fila'])).get_text().split('/')[0])

            #Caso diferença de Troncos Máximo com a Mínima for maior que 9 setar quantidade mínima
            if (trunks_max - trunks_min) > 9:
                r = s.post(url_adm, files=monta_req_files(vonixHtml, fila['fila'], 2 if trunks_min < 0 else trunks_min, fila['period'][0], fila['period'][1]), timeout=20)
                print('***DIMINUI QUANTIDADE DE TRONCOS DE => {} PARA => {}!\n'.format(trunks_max, 2 if trunks_min < 0 else trunks_min))
                continue

            fila_espera = int(vonixHtml.find(id='auto_waiting').get_text())
            #Caso já tenha uma chamada em espera, aguardar 3 segundos e capturar novamente
            if fila_espera > 0:
                r = s.post(url_adm, files=monta_req_files(vonixHtml, fila['fila'], 2 if (trunks_max - fila_espera) < 0 else (trunks_max - fila_espera), fila['period'][0], fila['period'][1]), timeout=20)
                print('***CHAMADA EM ESPERA => {} DIMINUI QUANTIDADE DE TRONCOS DE => {} PARA => {}!\n'.format(fila_espera, trunks_max, 2 if (trunks_max - fila_espera) < 0 else (trunks_max - fila_espera)))
                time.sleep(5)
                continue

            print(WELCOME)
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
                #Setar para a quantidade máxima de Troncos disponível
                if trunks_max >= 60:
                    print('>>>QUANTIDADE MÁXIMA DE TRONCOS ATINGIDA => {}!\n'.format(trunks_max))
                    time.sleep(3)
                    continue
                qtd_troncos+=1

            if qtd_troncos > 0 and trunks_max < 60:
                try:
                    r = s.post(url_adm, files=monta_req_files(vonixHtml, fila['fila'], trunks_max + qtd_troncos, fila['period'][0], fila['period'][1]), timeout=20)
                    print('***AUMENTOU QUANTIDADE DE TRONCOS DE => {} PARA => {}!\n'.format(trunks_max, trunks_max + qtd_troncos))
                    time.sleep(qtd_troncos * 5)
                    break
                except Exception as e:
                    print('***ERRO REQUISIÇÃO POST!\n{}'.format(e))
                    continue
    s.close()
