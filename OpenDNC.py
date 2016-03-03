#!/usr/bin/env python

from lib import RS232DNC

class OpenDNC:
  def __init__(self, args):
    self.args = args
    self.validateArgs()
    
  def validateArgs(self):
    pass

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
      'FILE-NAME',
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
      help="set parity, one of {N E O S M}, default: N",
      default='N')

  group.add_argument(
      '--rtscts',
      action='store_true',
      help='enable RTS/CTS flow control (default off)',
      default=False)

  group.add_argument(
      '--xonxoff',
      action='store_true',
      help='enable software flow control (default on)',
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
      help='set baud rate (default: 9600)',
      default=9600)

  args = parser.parse_args()

  openDNC = OpenDNC(args)

  print("OpenDNC Finished!")
  