import socket
import binascii
from utils import *
from pacoteMXT import*

HOST = ''     # Endereco IP do Servidor
PORT = 5714            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(10)

print "GATEWAY FELIPE"
while True:
    con, cliente = tcp.accept()
    print 'Conectado por', cliente
    while True:
        msg = con.recv(1024)
        if not msg: break
        pct = PacoteMXT(msg)
        pct.exibir_infos()
        con.send(pct.pacote_ack)
    print 'Finalizando conexao do cliente', cliente
    con.close()