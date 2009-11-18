""" Wrapper for pygame, which exports the PSP Python API on non-PSP systems. """

__author__ = 'Boris Buegling, <boris@icculus.org>'

import pygame

pygame.init()

volume = -1
volume2 = -1

def setMusicVolume (vol):
  volume = vol

def setSndFxVolume (vol):
  volume2 = vol

class Music:
  def __init__ (self, fname, loop=False):
    self._loop = loop
    # TODO: Support for xm
    #self._snd = pygame.mixer.Sound(fname.replace('xm', 'wav'))
    self._snd = pygame.mixer.music.load(fname)
    if not volume == -1:
      self._snd.set_volume(volume)

  def start (self):
    return
    if self._loop:
      self._snd.play(-1)
    else:
      self._snd.play()

  def stop (self):
    # TODO: Implement this.
    pass

class Sound:
  def __init__ (self, filename):
    #pygame.mixer.pre_init(44100,8,0)
    pygame.mixer.init()
    try:
      self._snd = pygame.mixer.Sound(filename)
      if not volume == -1:
        self._snd.set_volume(volume2)
    except:
      print "Error Loading: " + filename
      self._snd = None

  def start (self):
    if self._snd:
      self._snd.play()
