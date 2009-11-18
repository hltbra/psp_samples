#!/usr/bin/python
""" Wrapper for PyGame, which exports the pspnet API on non-PSP systems. """

__author__ = 'Boris Buegling, <boris@icculus.org>'
import time, thread
from socket import gethostbyname, gethostname

state = 0
def connectToAPCTL(n = 1, callback = None, timeout=-1):
  thread.start_new_thread(__connectToAPCTL , (n, callback))

def __connectToAPCTL(n = 1, callback = None, timeout=-1):
  global state
  if callback:
    callback(0)
    state = 0
  time.sleep(0.2)
  if callback:
    callback(2)
    state = 2
  time.sleep(0.2)
  if callback:
    callback(3)
    state = 3
  time.sleep(0.2)
  if callback:
    callback(4)
    state = 4
  time.sleep(0.2)
  if callback:
    callback(-1)
    state = 4

def disconnectAPCTL ():
  pass

def getIP():
  return gethostbyname(gethostname())

if __name__ == '__main__':
  print getIP()

def enumConfigs():
  return ([(1, "Connessione 1", 0), (2, "Connessione 2", 0)])

def wlanSwitchState():
  return True

def getAPCTLState():
  return state
