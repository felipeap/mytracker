def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install',package])
    finally:
        globals()[package] = importlib.import_module(package)

print "INSTALLING PACKAGES"
install_and_import('pymongo')
install_and_import('crcmod')
install_and_import('bson')
install_and_import('jsonutil')

print "INSTALLED"

import datetime
import asyncore, socket
from pacoteMXT import *

class Server(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('', port))
        self.listen(5)

    def handle_accept(self):
        # when we get a client connection start a dispatcher for that
        # client
        socket, address = self.accept()
        print "Connection by" + str(address)
        EchoHandler(socket)

class EchoHandler(asyncore.dispatcher_with_send):
    # dispatcher_with_send extends the basic dispatcher to have an output
    # buffer that it writes whenever there's content
    def handle_read(self):
        self.out_buffer = self.recv(1024)
        print " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        text_file = open("/home/pi/GatewayMxt/GtwLogs/log.txt", "a")
        pacote = str(datetime.datetime.now()) + " -- " + str(self.out_buffer.__len__()) + "   "+ binascii.hexlify(self.out_buffer)
        print pacote
        text_file.write(pacote + "\n")
        text_file.close()
        if not self.out_buffer:
            self.close()
        if self.out_buffer.__len__() > 0:
            pct = PacoteMXT(self.out_buffer)
            self.out_buffer = ''
            self.send(pct.pacote_ack)

print "INIT  GATEWAY  FELIPE"
s = Server('', 21025)
asyncore.loop()
