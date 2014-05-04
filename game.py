import pyglet, sys, select
from pyglet.gl import *
from base64 import b64encode, b64decode
from os.path import isfile, abspath
from collections import OrderedDict
from socket import *
from json import loads, dumps
from threading import *
from time import sleep

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_LINE_SMOOTH)
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
pyglet.options['audio'] = ('alsa', 'openal', 'silent')
key = pyglet.window.key

class cube():
	def __init__(self):
		self.xpos = 100
		self.ypos = 100
		self.anglex, self.angley, self.anglez = 0, 0, 0
		self.size = 2
		self.texture = pyglet.image.load('square.jpg').get_texture()
		x = 30/2.0
		y = 30/2.0
		self.vlist = pyglet.graphics.vertex_list(4, ('v2f', [-x,-y, x,-y, -x,y, x,y]), ('t2f', [0,0, 1,0, 0,1, 1,1]))

	def _draw(self):
		glPushMatrix()
		glTranslatef(self.xpos, self.ypos, 0)
		#glRotatef(self.anglex, self.anglex, self.angley, self.anglez)
		glRotatef(self.anglex, 1, 0, 0)
		glRotatef(self.angley, 0, 1, 0)
		glRotatef(self.anglez, 0, 0, 1)
		glScalef(self.size, self.size, self.size)
		glColor3f(1,1,1)
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, self.texture.id)
		self.vlist.draw(GL_TRIANGLE_STRIP)
		glDisable(GL_TEXTURE_2D)
		glPopMatrix()

class GUI(pyglet.window.Window):
	def __init__(self):
		super(GUI, self).__init__(640,800, caption='Shatt')
		self.alive = True

		self.graphics = OrderedDict()
		self.graphics['cube'] = cube()
		
		self.keymodifiers = {'shift' : False, 'ctrl' : False, 'alt' : False, 'altgr' : False}
		self.keydown = {}

		self.drag = False
		self.active = None, None
		self.alive = 1
		self.multiselect = False
		self.merge_sprites = {}

		glClearColor(0, 0.3, 0.5, 0)
		glClear(GL_COLOR_BUFFER_BIT)


	def render(self, *args):
		self.clear()
		for item in self.graphics:
			self.graphics[item]._draw()
		self.flip()

	def on_draw(self):
		self.render()

	def on_close(self):
		self.alive = False

	def on_mouse_release(self, x, y, button, modifiers):
		if button == 1:
			if self.active[1] and not self.drag and self.multiselect == False:
				self.active[1].click(x, y, self.merge_sprites)
				if self.active[0] == 'menu':
					del(self.graphics['menu'])
			self.drag = False
		elif button == 4:
			if not self.active[0]:
				pass #Do something on empty spaces?
			else:
				self.active[1].right_click(x, y, self.merge_sprites)
	
	def on_mouse_press(self, x, y, button, modifiers):
		if button == 1 or button == 4:
			for sprite_name, sprite in self.graphics.items():
				if sprite:
					sprite_obj = sprite.click_check(x, y)
					if sprite_obj:
						self.active = sprite_name, sprite_obj
						if button == 1:
							if self.multiselect != False:
								if sprite_name not in self.multiselect:
										self.multiselect.append(sprite_name)

	def on_mouse_motion(self, x, y, dx, dy):
		pass

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		pass

	def on_key_press(self, symbol, modifiers):
		remap = {146028888064 : 229,
				206158430208 : 228,
				201863462912 : 246}
		if symbol in remap:
			symbol = remap[symbol]
		if symbol == 65307: # [ESC]
			for obj in self.graphics:
				self.graphics[obj].escape()
		elif symbol == key.LSHIFT:
			symbol = 'shift'
		elif symbol == key.LCTRL:
			self.multiselect = []
		elif symbol == 65362: # up
			symbol = 'up'
			#self.graphics['cube'].angley += 0.1
		elif symbol == 65364: # down
			symbol = 'down'
			#self.graphics['cube'].angley -= 0.1
		elif symbol == 65361: # left
			symbol = 'left'
			#self.graphics['cube'].anglex += 0.1
		elif symbol == 65363: # right
			symbol = 'right'
			#self.graphics['cube'].anglex -= 0.1
		else:
			try:
				symbol = chr(symbol)
			except:
				pass

		self.keydown[symbol] = True

	def on_key_release(self, symbol, modifiers):
		remap = {146028888064 : 229,
				206158430208 : 228,
				201863462912 : 246}
		if symbol in remap:
			symbol = remap[symbol]

		if symbol == key.LCTRL:
			self.multiselect = False
		elif symbol == 65307: # [ESC]
			for obj in self.graphics:
				self.graphics[obj].escape()
		elif symbol == key.LSHIFT:
			symbol = 'shift'
		elif symbol == key.LCTRL:
			self.multiselect = []
		elif symbol == 65362: # up
			symbol = 'up'
			#self.graphics['cube'].angley += 0.1
		elif symbol == 65364: # down
			symbol = 'down'
			#self.graphics['cube'].angley -= 0.1
		elif symbol == 65361: # left
			symbol = 'left'
			#self.graphics['cube'].anglex += 0.1
		elif symbol == 65363: # right
			symbol = 'right'
			#self.graphics['cube'].anglex -= 0.1
		else:
			try:
				symbol = chr(symbol)
			except:
				pass

		self.keydown[symbol] = False

	def run(self):
		while self.alive:
			event = self.dispatch_events()

			if event:
				print(event)

			for key in list(self.keydown.keys()):
				if self.keydown[key] == False:
					del(self.keydown[key])
					continue

				if key == 'up':
					self.graphics['cube'].angley += 0.1
				elif key == 'down':
					self.graphics['cube'].angley -= 0.1
				elif key == 'left':
					self.graphics['cube'].anglex += 0.1
				elif key == 'right':
					self.graphics['cube'].anglex -= 0.1
				elif key == 'z':
					self.graphics['cube'].anglez -= 0.1

			self.render()

x = GUI()
pyglet.clock.set_fps_limit(60)
x.run()