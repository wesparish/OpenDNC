#!/usr/bin/env python

import logging
import logging.config
from logging.handlers import RotatingFileHandler

class OpenDNCLogger(object):
  def __init__(self):
    logging.config.fileConfig('../conf/logging.conf')
    
    # create _logger
    self._logger = logging.getLogger('openDNC')

class TestDriver(OpenDNCLogger):
  def __init__(self):
    super(TestDriver, self).__init__()
  
  def runTests(self):
    self._logger.debug('debug OpenDNCLogger Initialized')
    self._logger.info('info OpenDNCLogger Initialized')
    self._logger.warn('warn OpenDNCLogger Initialized')
    self._logger.error('error OpenDNCLogger Initialized')
    self._logger.critical('critical OpenDNCLogger Initialized')    

if __name__ == "__main__":
  testDriver = TestDriver()
  testDriver.runTests()