 #!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class in Python 2.7 that executes a Thread for reading RFID tags.
Credits and License: Created by Erivando Sena

 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License.
"""

import threading
from time import sleep
from module.nfc_522 import Nfc522
import finalcode as func 
from bcolors import bcolors



__author__ = "Erivando Sena Ramos"
__copyright__ = "Erivando Sena (2016)"
__email__ = "erivandoramos@bol.com.br"
__status__ = "Prototype"


class LeitorCartao(threading.Thread):
    
    nfc = Nfc522()
    numero_cartao = None
    
    def __init__(self, intervalo=0.2):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        self._sleepperiod = intervalo
        self.name = 'Reader Thread'
        
    def run(self):
        print "%s. Running " % self.name
        while not self._stopevent.isSet():
            self.ler()
            self._stopevent.wait(self._sleepperiod)
        print "Turning off %s" % (self.getName(),)

        func.closeConnection()#close function call here
        
        
    def obtem_numero_cartao_rfid(self):
        id = None
        try:
            while True:
                [gpio_port, id] = self.nfc.obtem_nfc_rfid()
                if id:
                    id = str(id).zfill(10)
                    if (len(id) >= 10):
                        self.numero_cartao = id
                        
                        return [gpio_port, self.numero_cartao]
                    else:
                        print "Error TAG Number: " +str(self.numero_cartao)
                        id = None
                        return [gpio_port, None]
                else:
                    return [gpio_port, id]
        except Exception as e:
            print e
            
    def ler(self):
        try:
            [gpio_port, tagId] = self.obtem_numero_cartao_rfid()
            if tagId:
                self.valida_cartao(gpio_port, self.numero_cartao)
            else:
                return None
        except Exception as e:
            print e
            
    def valida_cartao(self, gpio_port, tagId):
        try:            
            func.enOrExCarData(gpio_port, tagId) #generate car data function called here            
             

        except Exception as e:
            print 'Error: ',e
			
