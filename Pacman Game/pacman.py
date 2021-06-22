# pacman.py

from tkinter import *
from PIL import Image, ImageTk
import random
from map import map1

MOVE_INCREMENT = 20
MOVE_PER_SECOND = 5
GAME_SPEED = 1000 // MOVE_PER_SECOND

class Pacman(Canvas):
	def __init__(self):
		super().__init__(width = 720, height = 400, background = 'black', highlightthickness = 0)

		self.pacman_position = (360, 220)
		self.ghost_positions = [(340, 60), (360, 60), (380, 60), 
								(340, 360), (360, 360), (380, 360)]
		self.map_positions = map1
		self.all_fruit = 0
		self.fruit_positions = self.set_new_fruit_position()
		self.score = 0
		self.loop = None
		self.direction = 'static'
		self.starting = False
		self.ending = False

		self.bind_all('<Key>', self.on_key_press)

		self.load_assets()
		self.create_objects()
		self.rungame()

	def load_assets(self):
		self.pacman_body_image = Image.open('./assets/body.png')
		self.pacman_body = ImageTk.PhotoImage(self.pacman_body_image)

		self.ghost_body_image = Image.open('./assets/ghost.png')
		self.ghost_body = ImageTk.PhotoImage(self.ghost_body_image)

		self.fruit_body_image = Image.open('./assets/fruit.png')
		self.fruit_body = ImageTk.PhotoImage(self.fruit_body_image)

		self.map_image = Image.open('./assets/map.png')
		self.map = ImageTk.PhotoImage(self.map_image)

	def create_objects(self):
		FONT = (None, 14)
		self.create_text(45, 12, text = 'Score: {}'.format(self.score), tag = 'score', fill = 'white', font = FONT)

		self.create_image(*self.pacman_position, image = self.pacman_body, tag = 'pacman')

		for x_pos , y_pos in self.fruit_positions:
			self.create_image(x_pos, y_pos, image = self.fruit_body, tag = 'fruit' + str(x_pos) + str(y_pos))

		no_ghost = 0
		for x_pos , y_pos in self.ghost_positions:
			self.create_image(x_pos, y_pos, image = self.ghost_body, tag = 'ghost' + str(no_ghost))
			no_ghost += 1

		for x_pos , y_pos in self.map_positions:
			self.create_image(x_pos, y_pos, image = self.map, tag = 'map')

		self.create_rectangle(7, 27, 713, 393, outline = '#FFF')

	def move_pacman(self):
		x_pos, y_pos = self.pacman_position

		if self.check_pacman_collisions() or self.check_pacman_map_collisions():
			self.direction = 'static'

		if self.direction == 'Up':
			new_pos = (x_pos, y_pos - MOVE_INCREMENT)
		elif self.direction == 'Down':
			new_pos = (x_pos, y_pos + MOVE_INCREMENT)
		elif self.direction == 'Right':
			new_pos = (x_pos + MOVE_INCREMENT, y_pos)
		elif self.direction == 'Left':
			new_pos = (x_pos - MOVE_INCREMENT, y_pos)
		elif self.direction == 'static':
			new_pos = (x_pos, y_pos)

		if self.direction != 'static':
			self.starting = True

		self.pacman_position = new_pos

		self.coords(self.find_withtag('pacman'), *self.pacman_position)

	def move_ghost(self):
		index_gost = 0
		chance_follow = 2
		if self.all_fruit - self.score <= 40:
			chance_follow = 1

		for x_pos, y_pos in self.ghost_positions:
			randmove_or_follow = random.randint(0, 4)

			if randmove_or_follow <= chance_follow:
				rand_move = random.randint(0, 4)

				if rand_move == 0:
					new_pos = (x_pos, y_pos - MOVE_INCREMENT)
				elif rand_move == 1:
					new_pos = (x_pos, y_pos + MOVE_INCREMENT)
				elif rand_move == 2:
					new_pos = (x_pos + MOVE_INCREMENT, y_pos)
				else:
					new_pos = (x_pos - MOVE_INCREMENT, y_pos)
			else:
				randmove_way = random.randint(0, 2)

				move = 0
				if x_pos <= self.pacman_position[0] and y_pos <= self.pacman_position[1]:
					if randmove_way == 0:
						move = 1
					else:
						move = 2
				elif x_pos >= self.pacman_position[0] and y_pos <= self.pacman_position[1]:
					if randmove_way == 0:
						move = 1
					else:
						move = 3
				elif x_pos <= self.pacman_position[0] and y_pos >= self.pacman_position[1]:
					if randmove_way == 0:
						move = 0
					else:
						move = 2
				elif x_pos >= self.pacman_position[0] and y_pos >= self.pacman_position[1]:
					if randmove_way == 0:
						move = 0
					else:
						move = 3

				if move == 0: # Up
					new_pos = (x_pos, y_pos - MOVE_INCREMENT)
				elif move == 1: # Down
					new_pos = (x_pos, y_pos + MOVE_INCREMENT)
				elif move == 2: # Right
					new_pos = (x_pos + MOVE_INCREMENT, y_pos)
				else: # Left
					new_pos = (x_pos - MOVE_INCREMENT, y_pos)


			self.ghost_positions[index_gost] = new_pos

			if self.check_ghost_collisions(index_gost) or self.check_ghost_map_collisions(index_gost):
				self.ghost_positions[index_gost] = (x_pos, y_pos)

			self.coords(self.find_withtag('ghost' + str(index_gost)), *self.ghost_positions[index_gost])
			index_gost += 1

	def on_key_press(self, e):
		new_direction = e.keysym

		all_direction = ('Up', 'Down', 'Left', 'Right')
		if new_direction in all_direction:
			self.direction = new_direction
		elif new_direction == 'F1':
			self.rungame()

	def check_ghost_map_collisions(self, index_gost):
		x_pos, y_pos = self.ghost_positions[index_gost]

		if (x_pos, y_pos) in self.map_positions:
			return True
		return False

	def check_ghost_collisions(self, index_gost):
		x_pos, y_pos = self.ghost_positions[index_gost]

		return (x_pos in (0, 720) or y_pos in (20, 400))

	def check_pacman_map_collisions(self):
		x_pos, y_pos = self.pacman_position

		if self.direction == 'Up':
			y_pos -= 20
		elif self.direction == 'Left':
			x_pos -= 20
		elif self.direction == 'Right':
			x_pos += 20
		elif self.direction == 'Down':
			y_pos += 20

		if (x_pos, y_pos) in self.map_positions:
			return True
		return False

	def check_pacman_collisions(self):
		x_pos, y_pos = self.pacman_position

		if x_pos == 20 and y_pos == 40 and (self.direction == 'Up' or self.direction == 'Left'):
			return True
		elif x_pos == 700 and y_pos == 40 and (self.direction == 'Up' or self.direction == 'Right'):
			return True
		elif x_pos == 20 and y_pos == 380 and (self.direction == 'Down' or self.direction == 'Left'):
			return True
		elif x_pos == 700 and y_pos == 380 and (self.direction == 'Down' or self.direction == 'Right'):
			return True
		elif y_pos == 40 and self.direction == 'Up':
			return True
		elif x_pos == 20 and self.direction == 'Left':
			return True
		elif x_pos == 700 and self.direction == 'Right':
			return True
		elif y_pos == 380 and self.direction == 'Down':
			return True
		return False

	def check_fruit_collisions(self):
		if self.pacman_position in self.fruit_positions:
			self.score += 1
			self.fruit_positions.remove((self.pacman_position[0], self.pacman_position[1]))

			score = self.find_withtag('score')
			self.itemconfigure(score, text = 'Score: {}'.format(self.score))

			self.delete('fruit' + str(self.pacman_position[0]) + str(self.pacman_position[1]))

	def set_new_fruit_position(self):
		fruit_positions = []
		for x_pos in range(1, 36):
			for y_pos in range(2, 20):
				if ((x_pos * 20, y_pos * 20) != self.pacman_position) and ((x_pos * 20, y_pos * 20) not in self.map_positions):
					fruit_positions.append((x_pos * 20, y_pos * 20))
					self.all_fruit += 1

		return fruit_positions

	def rungame(self):
		if self.score == self.all_fruit and self.ending == False:
			self.ending = True
			self.after_cancel(self.loop)
			self.delete('all')
			self.create_text(360, 220, justify = CENTER,
                             text = f'You Win!!\n\nScore: {self.score}\n\nNew Game <F1>',
                             fill = 'yellow', font = (None, 30))

		elif self.pacman_position in self.ghost_positions and self.ending == False:
			self.ending = True
			self.after_cancel(self.loop)
			self.delete('all')
			self.create_text(360, 200, justify = CENTER,
                             text = f'GAME OVER\n\nScore: {self.score}\n\nNew Game <F1>',
                             fill = 'yellow', font = (None, 30))

		elif self.ending == True:
			self.ending = False
			self.delete('all')
			self.pacman_position = (360, 220)
			self.ghost_positions = [(340, 60), (360, 60), (380, 60), 
									(340, 360), (360, 360), (380, 360)]
			self.map_positions = map1

			self.all_fruit = 0
			self.fruit_positions = self.set_new_fruit_position()
			self.score = 0
			self.loop = None
			self.direction = 'static'
			self.starting = False
			self.ending = False

			self.create_objects()
			self.loop = self.after(GAME_SPEED, self.rungame)
		else:
			self.move_pacman()
			self.check_fruit_collisions()
			if self.starting == True:
				self.move_ghost()

			self.loop = self.after(GAME_SPEED, self.rungame)


GUI = Tk()
GUI.title('Pacman Game by nomomon')
GUI.resizable(False, False)

game = Pacman()
game.pack()

GUI.mainloop()