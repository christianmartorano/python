import socket
import subprocess
import shlex
import os
import sys
from optparse import OptionParser

WELCOME_MESSAGE = """
  _____    __ __      ___ _      _
 /  ___/  |  T  T   /   _] T    | T
(   \_    |  l  |  /   [_| |    | |
 \__   T  |  _  | Y    _ ] l___ | l___
/   \  |  |  |  | |   [_ |     T|     T
\      |  |  |  | |     T|     ||     |
 \_____j  l__j__j l_____jl_____jl_____j"""

ip = '127.0.0.1'
porta = 2222

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((ip,porta))

s.listen(1)

conn, addr = s.accept()

conn.send(WELCOME_MESSAGE.encode('utf-8'))
conn.send('\n\n>>> Type close_shell to close the connection.\n'.encode('utf-8'))

print('>>> Connection from %s:%d' % (addr[0],addr[1]))

while True:
    conn.send('>>> '.encode('utf-8'))
    msg = conn.recv(1024)

    if len(msg) > 1024:
        conn.send('\n>>> Max command length accepted is 1024 bytes.'.encode('utf-8'))
        continue

    print('>>> From %s:%d receveid the command: %s' % (addr[0],addr[1],msg.decode('utf-8')))

    if 'close_shell' in msg.decode('utf-8'):
        conn.close()
        break

    if 'cd' in msg.decode('utf-8'):
        dir = msg.decode('utf-8').replace('cd','').lstrip().splitlines()
        if os.access(dir[0],os.R_OK) == False:
            msg = ('>>> Directory %s not Found!\n' % dir[0] ).encode('utf-8')
        else:
            os.chdir(dir[0])
            msg = ('>>> Actual directory is %s' % os.getcwd()).encode('utf-8')
        conn.send(msg)
        continue

    res = subprocess.Popen(shlex.split(msg.decode('utf-8')),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out = res.communicate()

    if any(out[0]):
        for line in out[0].splitlines():
            msg = ('>>> %s\n' % line.decode('utf-8'))
            conn.send(msg.encode('utf-8'))
    else:
        for line in out[1].splitlines():
            msg = ('>>> %s\n' % line.decode('utf-8'))
            conn.send(msg.encode('utf-8'))

print('>>> Closing the Server! Bye!')
s.close()
