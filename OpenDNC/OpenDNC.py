#!/usr/bin/env python

import os
from lib.RS232DNC import RS232DNC
from time import sleep
import logging
from lib.OpenDNCLogger import OpenDNCLogger

class OpenDNC(OpenDNCLogger):
  def __init__(self, args):
    self.args = args
    self.validateArgs()
    self.logConfigFile = "%s/%s" % (os.path.dirname(os.path.realpath(__file__)), 
                               "conf/logging.conf")
    super(OpenDNC, self).__init__(logConfigFile=self.logConfigFile)
    
  def validateArgs(self):
    pass
  
  def run(self):
    rs232DNC = RS232DNC(
               port=self.args.SERIALPORT, baudrate=self.args.baud_rate, 
               bytesize=self.args.byte_size, parity=self.args.parity,
               stopbits=self.args.stop_bits, timeout=self.args.timeout, 
               xonxoff=self.args.xonxoff, rtscts=self.args.rtscts, 
               openImmediately=True, newlineChar=self.args.newline_char, 
               lineBuffering=True, logConfigFile=self.logConfigFile)
    if self.args.OPERATION.lower() == "send":
      with open (self.args.FILENAME, "r") as fileToSend:
        try:
          rs232DNC.sendData(fileToSend.read().encode())
        except Exception as ex:
          self._logger.error(ex.message)
          raise
        
    elif self.args.OPERATION.lower() == "receive":
      try:
        print("\nPress ctrl+c to quit app when finished receiving data\nReady to receive data...\n")
        # Change log level above debug so we don't spam while looping
        if self._logger.level < logging.WARNING:
          previousLogLevel = self._logger.level
          self._logger.setLevel(logging.WARNING)
        
        with open (self.args.FILENAME, "w+") as fileToWrite:
          while True:
            inputData = rs232DNC.receiveData()
            if inputData:
              fileToWrite.write(inputData)
              print(inputData)
            sleep(0.5)
      except KeyboardInterrupt as ex:
        fileToWrite.close()
        self._logger.setLevel(previousLogLevel)
      except Exception as ex:
        self._logger.error(ex.message)
        raise
    
    rs232DNC.closeSerialPort()

if __name__ == "__main__":
  import argparse
  print("OpenDNC Starting...")
  
  parser = argparse.ArgumentParser(
        description='Simple DNC application for CNC machines',
        epilog="""\
NOTE: This program is currently in BETA - no warranty of any kind is
implied. Use of this program may cause harm to you or your machine tool and
may cause Skynet to launch an attack on mankind.
""")

  parser.add_argument(
      'SERIALPORT',
      help="serial port name")
  
  parser.add_argument(
      'OPERATION',
      help="operation to perform (possible values: send, receive)")
  
  parser.add_argument(
      'FILENAME',
      help="file to send or receive")

  parser.add_argument(
      '-q', '--quiet',
      action='store_true',
      help='suppress non error messages',
      default=False)

  group = parser.add_argument_group('serial port')

  group.add_argument(
      "--parity",
      choices=['N', 'E', 'O', 'S', 'M'],
      type=lambda c: c.upper(),
      help="set parity, one of {N E O S M}, default: E",
      default='E')

  group.add_argument(
      '--rtscts',
      action='store_true',
      help='enable RTS/CTS flow control (default off)',
      default=False)

  group.add_argument(
      '--xonxoff',
      action='store_false',
      help='disable software flow control (default on)',
      default=True)

  group.add_argument(
      '--rts',
      type=int,
      help='set initial RTS line state (possible values: 0, 1)',
      default=None)

  group.add_argument(
      '--dtr',
      type=int,
      help='set initial DTR line state (possible values: 0, 1)',
      default=None)

  group.add_argument(
      '--baud-rate',
      type=int,
      help='set baud rate (default: 2400)',
      default=2400)

  group.add_argument(
      '--byte-size',
      type=int,
      help='set byte size (default: 7)',
      default=7)

  group.add_argument(
      '--stop-bits',
      type=int,
      help='set stop bits (default: 1)',
      default=1)

  group.add_argument(
      '--timeout',
      type=int,
      help='set timeout in seconds (default: None)',
      default=None)

  group.add_argument(
      '--newline-char',
      type=int,
      help='set newline char (default: \'\', options: \'\', \'\\n\''
           ', \'\\r\', and \'\\r\\n\')',
      default=None)

  args = parser.parse_args()

  openDNC = OpenDNC(args)
  openDNC.run()

  print("OpenDNC Finished!")
  