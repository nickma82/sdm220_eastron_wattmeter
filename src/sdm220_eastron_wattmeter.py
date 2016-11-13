#!/usr/bin/env python

import minimalmodbus
import serial
from random import randint

__author__  = "Nick Ma"

class SDM220DataElement():
    def __init__(self, address, unit, valid_for_ms=1000):
        self.address = address
        self.unit = str(unit)
        self.valid_for_ms = valid_for_ms

        self.value = 0

    def __str__(self):
        return str(self.value)

class EastronSDM220Base:
    dataMemory = {
        'Voltage': SDM220DataElement(0x0000, 'U'),
        'Current': SDM220DataElement(0x0006, 'I'),
        'Active power': SDM220DataElement(0x000C, 'W'),
        'Apparent power': SDM220DataElement(0x0012, 'VA'),
        'Reactive power': SDM220DataElement(0x0018, 'VAr'),
        'Power factor': SDM220DataElement(0x001E, '-'),
        'Phase angle': SDM220DataElement(0x0024, 'Deg'),
        'Frequency': SDM220DataElement(0x0046, 'Hz'),
        'Import active energy': SDM220DataElement(0x0048, 'kWh'),
        'Export active energy': SDM220DataElement(0x004A, 'kWh'),
        'Import reactive energy': SDM220DataElement(0x4C, 'kVArh'),
        'Export reactive energy': SDM220DataElement(0x4E, 'kVArh'),
        'Total active energy': SDM220DataElement(0x0156, 'kWh'),
        'Total reactive energy': SDM220DataElement(0x0158, 'kVArh'),
        }


    def _update_singel(self, key):
        raise Exception('To be implemented in derived class')

    def _update_all(self):
        raise Exception('To be implemented in derived class')


    def get_single_value(self, key):
        self._update_singel(key)

        element = self.dataMemory.get(key)
        return None if (element is None) else element.value
        
    def get_all_values(self):
        self._update_all()
        return [(key, element.value, element.unit) for key,element in self.dataMemory.iteritems()]
        
class EastronSDM220Modbus(EastronSDM220Base, minimalmodbus.Instrument):
    HOLDINGREG_OFFSET = 10000

    def __init__(self, portname, slaveaddress=1):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)

        self.serial.baudrate = 9600
        self.serial.parity = serial.PARITY_EVEN
        self.serial.timeout = 0.1

        self.mode = minimalmodbus.MODE_RTU

    def _default_readout(self, registerAddress):
        return self. read_float(registerAddress, functioncode=4, numberOfRegisters=2)

    def _update_singel(self, key):
        element = self.dataMemory.get(key)
        if element is not None:
            element.value = self._default_readout(element.address)

    def _update_all(self):
        for key,element in self.dataMemory.iteritems():
            element.value = self._default_readout(element.address)

class EastronSDM220FakeValues(EastronSDM220Base):
    def _update_singel(self, key):
        element = self.dataMemory.get(key)
        if element is not None:
            element.value = randint(101, 200)

    def _update_all(self):
        for key,element in self.dataMemory.iteritems():
            #TODO Check valid_for value
            element.value = randint(1, 100)

if __name__ == '__main__':
    minimalmodbus._print_out( 'TESTING Eastron sdm220 Connection')

    n = EastronSDM220FakeValues()
    #n = EastronSDM220Modbus('/dev/ttyUSB0')
    n.debug = True
    print( n )

    ## starting demo
    minimalmodbus._print_out( 'U:      {0}[{1}]'.format(n.get_single_value('Voltage'), 'V'))

    print( n.get_all_values() )
    #minimalmodbus._print_out( 'I:      {0}A'.format(n.get_I()))

    #minimalmodbus._print_out('carsten_test:         {0}'.format( n.carsten_test() ))
    #minimalmodbus._print_out( 'userVentSet:             {0}'.format( n.get_userVent()       ))
    #n.set_userVent()
    #minimalmodbus._print_out( 'userVentSet:             {0}'.format( n.get_userVent()       ))
    
    #minimalmodbus._print_out( 'DONE!' )

pass  