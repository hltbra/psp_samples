# -*- coding: iso-8859-1 -*-
#sfont.py
#a rewriting of SFont in python. Uses pygame, but the original used SDL so there's really no change at all except that the code is cleaner and probably slower. On the plus side you can now link SFonts into pygame projects.

#By Kousu <kousue ut gmuil dut cum> 2006, under a BSD license. SFont.c is under GPL but I don't think it applies because I didn't wind up using any of the code from it since it's such a simple format.

import pygame
#XXX should we init pygame?

import pygame
from pygame.locals import *

charString = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ"

class Font:
	"""
	A SFont file should be a normal picture file (PNGs work well though anything pygame can load can be used). It should contain, in order, these characters:
	! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ ` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
	Leave an extra row of pixels at the top. In this row, between each character, place a string of pink=(255,0,255) pixels to demark the edges of the pixels
	There is one extra restriction
	Todo:
	grab all subsurfaces at font-creation time, not afterwards
	#XXX should return the length as second in the tuples? len is calc'd twice now, could cut it down)
	#XXX There's inefficiency: ranges() is run twice for every render()
	#XXX check this for bad-data bugs. Would it completely assrape if you don't give enough chars? or if accidentally connect two strings of pink together?.
	Support \n by moving down a line (perhaps split along \n and calculate based on how many lines you get?)

	Speed up tricks:
		+make a write() method that writes directly instead of rendering first
		+use numeric to do the wiping of the pixel-alphas
		+assume the colour in between chars is the colorkey; then just set_colorkey() of the rendering surface; but this would break any per-pixel alphas present... :(... perhaps check for per-pixel alphas first?
	Read SFont.c, in particular figure out this part:
	//#width = mid(self.CharPos[c+1]) - mid(self.CharPos[c])?? #get distance between the centers of this char & the next
	//#src.x = mid(self.CharPos[x]) #the center of the character
	//#dst.x = pos - mid(self.CharPos[x]) #pos is kept at the end of the place to write to; have to shift back 1 width.... except appearantly only half the character instead.
	srcrect.w = dstrect.w =
	    (Font->CharPos[charoffset+2] + Font->CharPos[charoffset+1])/2 -
	    (Font->CharPos[charoffset] + Font->CharPos[charoffset-1])/2;
	srcrect.x = (Font->CharPos[charoffset]+Font->CharPos[charoffset-1])/2;
	dstrect.x = x - (float)(Font->CharPos[charoffset]
			      - Font->CharPos[charoffset-1])/2;

	SDL_BlitSurface(Font->Surface, &srcrect, Surface, &dstrect);
	"""
	def __init__(self, filename):
		"""Works like normal pygame.font.Font(): takes a file to load from and a size. Size is a bit broken so far, it just is the vertical size in pixels to scale all the letters to
		XXX Doesn't check if pygame is initialized! Will crash if it's not!
		Todo: wrap this so it falls back on self.font = pygame.font.SysFont("Times New Roman", 30) if it can't open? or would that be unpythonic?
		Todo: allow passing an initial-char arg so that it can cover a different section of chracters (e.g. cover some univocde)
		"""
		self.surface = pygame.image.load(filename)
		self.CharPos = [] #holds tuples representing the ranges where to find each character

		"""
		algo:
		find a pink to the left of a non-pink, this marks the start of the letter
		find a pink to the right of a non-pink, this marks the end

		Equivilently:
		Loop to the right until you find a non-pink, this marks the start of the letter
		loop to the right until you find a pink, this marks the end
		Save the ranges
		"""
		PINK = self.surface.get_at((0,0)) #the colour to be used to delimit characters
		#Tokenize the surface by the pinks at the top
		#note: the enumerate() call must be here to support the ickyness below
		pixels = enumerate(self.surface.get_at((i, 0)) for i in xrange(self.surface.get_width()))
		for i,pixel in pixels:
			#discard initial pink pixels...
			if pixel == PINK: continue
			start = i
			#discard non-pinks
			while pixel != PINK:
				try: #ick, such awful code
					i,pixel = pixels.next() #NOTE!!! the loop does not work like you think...
				except StopIteration: break
			end = i
			self.CharPos.append((start,end))
			#and do it all over again...

	def ranges(self, text): #XXX Kill me
		"Get a list of tuples representing the ranges needed to grab the chars out of self.surface for the given text"
		for c in text:
			#c = ord(c)-33 #-33 because no.33 should be the first character in the font
			try:
			  c = charString.index(c)
			except ValueError:
			  c = -1
			if 0<=c<=len(self.CharPos):
				yield self.CharPos[c]
			else: #spaces and non-printables are just taken as the stuff in between the first and second chars. This is how SFont.c does it, don't look at me.
				#yield (self.CharPos[0][1], self.CharPos[1][0])
				yield (0,10) #better way

	def size(self, text):
		"""Font.size(text) -> (width, height)

		Give the dimensions needed to draw the string in text
		"""
		width = 0
		height = self.surface.get_height()-1 #-1 to account for the row of pinks
		for range in self.ranges(text):
			width += range[1]-range[0]
		return width, height

	def write(self, surface, pos, text):
		"""Draw the text onto the surface at position pos=(x,y), just like in SFont.c

		I'm only putting this in here because of SFont... and because it is horribly slow
		otherwise due to the bottleneck in render().
		But yeah, it doesn't fit the pygame model."""
		size = self.size(text)
		loc = 0 #location in font file
		for c in text:
			try:
			  c = charString.index(c)
			except ValueError:
			  c = -1
			#c = ord(c)-33 #-33 because no.33 should be the first character in the font
			if 0<=c<=len(self.CharPos):
				range = self.CharPos[c]
				width = range[1]-range[0]
				char = self.surface.subsurface( (range[0], 1, width, size[1]) )
			else: #make a transparent spacer
				width = 10
				char = pygame.Surface((width,size[1]))
				char.set_alpha(0)
			surface.blit(char, (pos[0]+loc,pos[1]+0))
			loc+=width

	def render(self, text, antialias, background=(0,0,0,0)):
		"""Return a surface with the text rendered onto it using this font. Just like pygame.Font.render()
		If background is not given it defaults to being completely transparent.
		"""
		drawing = pygame.Surface(self.size(text)) #XXX how to avoid calling size() twice?
		drawing = drawing.convert(drawing.get_bitsize(), SRCALPHA)
		#zero out the per-pixel alphas because otherwise the default black background shows up
		drawing.fill(background)
		#draw
		self.write(drawing, (0,0), text)
		return drawing


if __name__=='__main__':
	pygame.init()
	surf = pygame.display.set_mode((300,200))
	surf.fill((255,0,255))
	f = Font("24P_Arial_NeonYellow.png")

	surf.blit(f.render("fyadfyad~fyad!!"), (0,0))
	pygame.display.flip()
	while 1:
		for e in pygame.event.get():
			if e.type==pygame.QUIT:
				import sys
				sys.exit()
