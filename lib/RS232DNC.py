#!/usr/bin/env python

import sys
import serial
from OpenDNCLogger import OpenDNCLogger

class RS232DNC(OpenDNCLogger):
  def __init__(self, port="/dev/ttyS0", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=True, rtscts=False):
    super(RS232DNC, self).__init__()
    self._serialPort = None
    self._port = port
    self._baudrate = baudrate
    self._bytesize = bytesize
    self._parity = parity
    self._stopbits = stopbits
    self._timeout = timeout
    self._xonxoff = xonxoff
    self._rtscts = rtscts
    
    self._serialPort = serial.Serial()

    if self._serialPort:
      self._serialPort.port = self._port
      self._serialPort.baudrate = self._baudrate
      self._serialPort.bytesize = self._bytesize
      self._serialPort.parity = self._parity
      self._serialPort.stopbits = self._stopbits
      self._serialPort.timeout = self._timeout
      self._serialPort.xonxoff = self._xonxoff
      self._serialPort.rtscts = self._rtscts
      self._logger.info("Created serial port: %s" % self._serialPort)
      
  def openSerialPort(self):
    self._logger.info("Opening serial port")
    try:
      self._serialPort.open()
    except Exception as ex:
      self._logger.critical(ex)
      raise
    
    self._logger.info("Serial port opened successfully!")
    
  def sendData(self, dataToSend):
    pass
  
  def receiveData(self, bytesToReceive = None):
    pass
    
  
if __name__ == "__main__":
  #print("Testing RS232DNC class...")
  
  rs232dnc = RS232DNC()
  rs232dnc.openSerialPort()
  
  #print("... done!")
  