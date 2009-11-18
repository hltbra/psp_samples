""" Wrapper for PyGame, which exports the psp2d API on non-PSP systems. """

__author__ = 'Boris Buegling, <boris@icculus.org>'

import pygame, sfont, sys, time, threading

pygame.init()
pygame.display.set_caption('PythonPSP player')
pygame.key.set_repeat(1, 1)

def Color (*args):
  # TODO: This should be a class w/ rw attrs red, green, blue, alpha.
  return args

class Controller:
  """ Mapping the PSP controlls to a keyboard and a mouse (for the analog stick):

      Triangle:   Keypad s
      Square:   Keypad x
      Circle:   Keypad x
      Cross:    Keypad z

      Start:    Keypad v
      Select:    Keypad c
      L-Trigger:  Keypad q
      R-Trigger:  Keypad w

      Home:    F4 (immediately quits)

    If someone needs it, I will add support for joy{stick,pads}. """

  def __init__ (self, grab=False):
    if grab:
      pygame.event.set_grab(True)
      pygame.mouse.set_visible(False)
    else:
      pygame.event.set_grab(False)
      pygame.mouse.set_visible(True)

    self._key = [0] * 323
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        self._key = pygame.key.get_pressed()
        if self._key[pygame.K_F4]:
          sys.exit(0)

  @property
  def circle (self):
    #return self._key[pygame.K_KP6]
    return self._key[pygame.K_x]
  @property
  def cross (self):
    #return self._key[pygame.K_KP2]
    return self._key[pygame.K_z]

  @property
  def triangle (self):
    #return self._key[pygame.K_KP8]
    return self._key[pygame.K_s]

  @property
  def square (self):
    #return self._key[pygame.K_KP4]
    return self._key[pygame.K_a]

  @property
  def l (self):
    return self._key[pygame.K_q]
    #return self._key[pygame.K_KP_DIVIDE]

  @property
  def r (self):
    return self._key[pygame.K_w]
    #return self._key[pygame.K_KP_MINUS]

  @property
  def start (self):
    #return self._key[pygame.K_KP0]
    return self._key[pygame.K_v]

  @property
  def select (self):
    #return self._key[pygame.K_KP_PERIOD]
    return self._key[pygame.K_c]

  @property
  def left (self):
    return self._key[pygame.K_LEFT]

  @property
  def right (self):
    return self._key[pygame.K_RIGHT]

  @property
  def up (self):
    return self._key[pygame.K_UP]

  @property
  def down (self):
    return self._key[pygame.K_DOWN]

  @property
  def analogX (self):
    xpos = pygame.mouse.get_pos()[0] * 256 / 480 - 127
    return 0 #xpos

  @property
  def analogY (self):
    ypos = pygame.mouse.get_pos()[1] * 256 / 272 - 127
    return 0 #ypos

class Font (sfont.Font):
  def __init__ (self, fname):
    sfont.Font.__init__(self, fname)

  def drawText (self, img, x, y, text):
    self.write(img, (x, y), text)

  def textHeight (self, c):
    return self.size(str(c))[1]

  def textWidth (self, c):
    return self.size(str(c))[0]

class Image (pygame.Surface):
  def __init__ (self, *args):
    if len(args) == 2:
      pygame.Surface.__init__(self, (args[0], args[1]), pygame.SRCALPHA, 32)
      self.set_alpha(255)
    else:
      if type(args[0]) is Image:
        surf = args[0]
      else:
        surf = pygame.image.load(args[0])
      pygame.Surface.__init__(self, (surf.get_width(), surf.get_height()),
        pygame.SRCALPHA, 32)
      self.blit(surf, surf.get_rect())

  def clear (self, color):
    self.fill(color)

  def blit (self, src, sx = 0, sy = 0, w = -1, h = -1, dx = 0, dy = 0, blend = False):
    # TODO: Implement 'blend'
    if type(dx) is float:
      print "dx is flota, should be integer"
    if type(dy) is float:
      print "dx is flota, should be integer"

    if type(sx) is tuple:
      pygame.Surface.blit(self, src, sx)
      return
    if dx == -1:
      dx = src.get_rect()[0]
    if dy == -1:
      dy = src.get_rect()[1]

    if type(sx) is int:
      if w == -1: w = src.width
      if h == -1: h = src.height
      tmp = src.subsurface(sx, sy, w, h)
      pygame.Surface.blit(self, tmp, (dx, dy))
      return
    pygame.Surface.blit(self, src, (dx, dy))


  def fillRect (self, x, y, w, h, color):
    # TODO: Implement this.
    pass

  def saveToFile (self, filename):
    pygame.image.save(self, filename)

  def putPixel (self, x, y, Color):
    # TODO: Implement this
    pass

  def getPixel (self, x, y):
    # TODO: Implement this
    pass

  @property
  def width (self):
    rect = self.get_rect()
    return rect[2] - rect[0]

  @property
  def height (self):
    rect = self.get_rect()
    return rect[3] - rect[1]

class Screen:
  def __init__ (self, width=480, height=272):
    self._screen = pygame.display.set_mode((width, height))

  def blit (self, img, sx=0, sy=0, sw=-1, sh=-1, dx=-1, dy=-1, blend=False, dw=-1, dh=-1):
    # TODO: Implement 'blend'
    if type(sx) is tuple:
      dx, dy = sx
      sx = 0
    rect = img.get_rect()
    h = rect[3] - rect[1]
    w = rect[2] - rect[0]

    if sw == -1: sw = w
    if sh == -1: sh = h
    if dx == -1: dx = rect[0]
    if dy == -1: dy = rect[1]
    if dw == -1: dw = w
    if dh == -1: dh = h

    tmp = img.subsurface(sx, sy, sw, sh)
    if dw != w or dh != h:
      tmp = pygame.transform.scale(tmp, (dw, dh))
    self._screen.blit(tmp, (dx, dy))

  def swap (self):
    pygame.display.flip()
    #time.sleep(0.005)
    pygame.event.pump()

  def clear (self, color):
    self._screen.fill(color)

  def fillRect (self, x, y, w, h, color):
    self._screen.fill((x,y,w,h), color)

  def saveToFile (self, filename):
    surf = pygame.display.get_surface()
    pygame.image.save(surf, filename)


  def putPixel (self, x, y, Color):
    # TODO: Implement this
    pass

  def getPixel (self, x, y):
    # TODO: Implement this
    pass

  @property
  def width (self):
    rect = self._screen.get_rect()
    return rect[2] - rect[0]

  @property
  def height (self):
    rect = self._screen.get_rect()
    return rect[3] - rect[1]

class Mask:
  """  This is a 2-dimensionnal bit field, intended to be used in collision detection.. """
  # TODO: Implement this.

  def __init__ (self, img, x, y, w, h, threshold):
    pass

  def collide (self, msk):
    pass

  def union (self, msk):
    pass

  def isIn (self, x, y):
    pass

TR_PLUS = 1
TR_MULT = 2
class Transform:
  """  A class used to make pixel-based transformations on images. """
  # TODO: Implement this.

  # Constants for type
  TR_PLUS, TR_MULT = range(0, 2)

  def __init__ (self, type, param=None):
    pass

  # def __init__ ((self, cb):

  def apply (self, img):
    pass

class BlitBatch:
  def __init__ (self):
    self._lst = []

  def add (self, img):
    self._lst.append(img)

  def blit (self):
    for img in self._lst:
      screen.blit(img.data.img, dx=img.data.x, dy=img.data.y)

class TimerThread (threading.Thread):
  def __init__ (self, func, timeout):
    threading.Thread.__init__(self)
    self.function = func
    self.timeout = timeout / 1000

  def run (self):
    while True:
      time.sleep(self.timeout)
      if not self.function():
        break

class Timer:
  def __init__ (self, timeout):
    self.thr = TimerThread(self.fire, timeout)

  def fire (self):
    raise NotImplementedError('Override in your subclasse.')

  def run (self):
    self.thr.start()
