#
# Este modulo escucha en una puerta serial, se definen eventos
# en base a patrones (regEx) del contenido leido, se testean
# secuencialemnte en el orden que dueron agregados
#
# pip install pyserial
#
import serial
import time
import re
import threading
import os.path
import traceback
from .logger import Logger

log=Logger("smallneuron.SnSerial")

def eventWait(snserial):
    try:
        log.info("reader started")
        fails=0
        while True:
            try:
                if not snserial.isOpen():
                    snserial.rotateOpen()
                log.perfMark("eventWait read_until")
                line = snserial.read_until(snserial.eol)
                fails=0
                for e in snserial.events:
                    if re.search(e[1], line) != None:
                        if snserial.eventManager == None:
                            log.error("Warning eventManager not defined")
                        else:
                            log.perfMark("eventWait putEvent start")
                            snserial.eventManager.putEvent(e[0], {"data": str(line)})
                            log.perfMark("eventWait putEvent end")
                        log.info("event ", e[0], line)
                        break
            except Exception as e:
                log.perfMark("eventWait Exception")
                fails=fails+1
                if fails > 10:
                    raise("Falla multiples veces lectura serial "+str(fails))
                log.warn("Reintentamos lectura "+str(e) )
                time.sleep(1)
                snserial.close()
                
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
        snserial.eventManager.putEvent("panic", str(e))



class SnSerial(serial.Serial):
    def __init__(self, eventManager, port, baudrate, bytesize, parity, stopbits, endofline: bytes = b"\r"):
        super().__init__(baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits)
        self.originalPort=port
        self.rotateOpen()
        self.eventManager = eventManager
        self.eol = endofline
        self.events = []
        log.info("start")
        
    def addEvent(self, event, pattern=".*"):
        self.events.append((event, pattern))

    def read_until(self, end_of_read_byte: bytes = b"\r"):
        line = b""
        c = b""
        while c != end_of_read_byte:
            c = self.read()
            log.perfMark("read_until readChar")
            line += c
        return line[:-1].decode("utf-8")

    def start(self):
        log.debug("SnSerial started")
        threading.Thread(target=lambda: eventWait(self)).start()

    # Intentara abrir la puerta termina con 0 (cero) y falla lo cambiara el final por 1 (uno)
    def rotateOpen(self):
        port=self.originalPort
        if not os.path.exists(port):
                port=port[:-1]+"1"
                log.debug("snserial port not exist, trying ",port)
        self.port=port # al parecer esto abre el puerto
        self.open()    # pero para estar seguro
        log.debug("snserial port:", port)


# Para pruebas
if __name__ == '__main__':
    print("Waiting for read")
    s=SnSerial( None, "/dev/ttyACM0", 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
    c = b""
    while c != b"\r":
        c=s.read()
        print( c.decode("utf-8"))

