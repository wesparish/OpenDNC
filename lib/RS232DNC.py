#!/usr/bin/env python

import serial
from OpenDNCLogger import OpenDNCLogger
from time import sleep
import io

class RS232DNC(OpenDNCLogger):
  def __init__(self, port="/dev/ttyS0", baudrate=9600, bytesize=8, parity='N',
               stopbits=1, timeout=None, xonxoff=True, rtscts=False, 
               openImmediately=False, newlineChar='', lineBuffering=True,
               logConfigFile='../conf/logging.conf'):
    super(RS232DNC, self).__init__(logConfigFile=logConfigFile)
    self._serialPort = None
    self._port = port
    self._baudrate = baudrate
    self._bytesize = bytesize
    self._parity = parity
    self._stopbits = stopbits
    self._timeout = timeout
    self._xonxoff = xonxoff
    self._rtscts = rtscts
    self._newlineChar = newlineChar
    self._lineBuffering = lineBuffering
    
    self._serialPort = serial.Serial()
    # newline controls how line endings are handled. 
    # It can be None, '', '\n', '\r', and '\r\n'
    self._ioTextWrapper = io.TextIOWrapper(io.BufferedRWPair(self._serialPort,
                                                             self._serialPort),
                                           newline=self._newlineChar,
                                           line_buffering=self._lineBuffering)

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
      
    if openImmediately:
      self.openSerialPort()

  '''
  openSerialPort - Opens the configured serial port
  Parameters:
  Returns:
  '''
  def openSerialPort(self):
    self._logger.info("Opening serial port")
    try:
      self._serialPort.open()
    except Exception as ex:
      self._logger.critical(ex)
      raise
    
    self._logger.info("Serial port opened successfully!")
    
  '''
  sendData - Sends data to serial port
  Parameters: dataToSend
  Returns: Number of bytes sent
  '''
  def sendData(self, dataToSend):
    self._logger.debug("Sending %s bytes of data to serial port: %s" % (len(dataToSend), self._serialPort.port))
    bytesWritten = None
    try:
      bytesWritten = self._serialPort.write(dataToSend)
    except Exception as ex:
      self._logger.critical(ex)
      raise
    
    self._logger.debug("Send successful! (%s bytes)" % (bytesWritten))
    return bytesWritten
    
  '''
  writeLine - Writes a line of ascii text to the serial port
  Parameters: strToSend
  Returns: Number of bytes sent
  '''
  def writeLine(self, strToSend):
    self._logger.debug("Sending %s bytes of data to serial port: %s" % (len(strToSend), self._serialPort.port))
    bytesWritten = None
    try:
      bytesWritten = self._ioTextWrapper.write(unicode(strToSend))
      self._ioTextWrapper.flush()
    except Exception as ex:
      self._logger.critical(ex)
      raise
    
    self._logger.debug("Send successful! (%s bytes)" % (bytesWritten))
    return bytesWritten
  
  '''
  receiveData - Receives data from serial port
  Parameters: bytesToReceive
  Returns: strReceived
  '''  
  def receiveData(self, bytesToReceive = None):
    self._logger.debug("Receiving %s bytes of data from serial port: %s" % (bytesToReceive, self._serialPort.port))
    strReceived = None
    
    # If not specified, read all bytes from buffer
    if not bytesToReceive:
      bytesToReceive = self._serialPort.inWaiting()
      
    try:
      strReceived = self._serialPort.read(bytesToReceive)
    except Exception as ex:
      self._logger.critical(ex)
      raise
    
    self._logger.debug("Read successful! (%s bytes)" % (len(strReceived)))
    return strReceived
  
  '''
  readLine - Reads one line of data from input buffer
  Parameters:
  Returns: strReceived
  '''  
  def readLine(self):
    self._logger.debug("Receiving one line of data from serial port: %s" % (self._serialPort.port))
    strReceived = None
    
    try:
      strReceived = self._ioTextWrapper.readline()
    except Exception as ex:
      self._logger.critical(ex)
      raise
    
    self._logger.debug("Read successful! (%s bytes)" % (len(strReceived)))
    return strReceived
  
  '''
  closeSerialPort - Closes the serial port
  Parameters:
  Returns:
  '''    
  def closeSerialPort(self):
    self._logger.info("Closing serial port")
    try:
      self._serialPort.close()
    except Exception as ex:
      self._logger.critical(ex)
      raise
    
    self._logger.info("Serial port closed successfully!")
    

# Test driver
if __name__ == "__main__":  
  rs232dnc = RS232DNC(port="/dev/tnt0")
  rs232dnc2 = RS232DNC(port="/dev/tnt1")
  rs232dnc2.openSerialPort()
  rs232dnc.openSerialPort()

  with open ("../test/fileToSend1.nc", "r") as testfile:
    rs232dnc.sendData(testfile.read())
    
  inData = rs232dnc2.readLine()
  print("Read line from serial: %s" % inData)
  inData = rs232dnc2.receiveData()
  print("Read data from serial: %s" % inData)
  rs232dnc.closeSerialPort()
  