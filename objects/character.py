import pyxel

from utils.platformer import Platformer
from utils.utils import Direction

MOVE_SPEED = 1

class Character(Platformer):
	def __init__(self, x, y) -> None:
		super(Character, self).__init__()

		self.width = 16
		self.height = 16
		self.x = x
		self.y = y
		self.animation_name = "idle_left"
		self.animations = {
			"idle_left": [[0, 16], [16, 16], [32, 16], [48, 16], [32, 16], [16, 16]],
			"idle_right": [[0, 32], [16, 32], [32, 32], [48, 32], [32, 32], [16, 32]],
			"walk_left": [[0, 48], [16, 48], [32, 48], [48, 48], [32, 48], [16, 48]],
			"walk_right": [[0, 64], [16, 64], [32, 64], [48, 64], [32, 64], [16, 64]],
			"jump_left": [[0, 80], [16, 80], [32, 80], [48, 80], [32, 80], [16, 80]],
			"jump_right": [[0, 96], [16, 96], [32, 96], [48, 96], [32, 96], [16, 96]],
			"fall_left": [[0, 112], [16, 112], [32, 112], [48, 112], [32, 112], [16, 112]],
			"fall_right": [[0, 128], [16, 128], [32, 128], [48, 128], [32, 128], [16, 128]],
			"hurt_left": [[0, 144], [16, 144], [32, 144], [48, 144], [0, 160], [16, 160], [32, 160], [48, 160]],
			"hurt_right": [[0, 176], [16, 176], [32, 176], [48, 176], [0, 192], [16, 192], [32, 192], [48, 192]],
			"happy": [[0, 208], [16, 208], [32, 208], [48, 208], [32, 208], [16, 208]],
		}
		self.tilemap = 0
		self.tile_width = 16
		self.tile_height = 16
		self.acceleration = 0.05
		self.jump_speed = 3.6
		self.max_dx = 1
		self.max_dy = 8
		self.bounce = 0.3
		self.x_direction = Direction.left
		self.margin.top = 3
		self.margin.left = 2
		self.margin.right = 2
		self.solid_tilemap = 0
		self.solid_list = [
			(8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2), (15, 2),
			(8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3), (15, 3),
			(8, 4), (9, 4),
			(8, 5), (9, 5),
		]
		self.is_flip = False
		self.is_hurt = False
		self.is_happy = False

	def update(self) -> None:
		super(Character, self).update()

		if self.x + self.margin.left < 0:
			self.x = -self.margin.left
		elif self.x + self.width - self.margin.right > 160:
			self.x = 160 - (self.width - self.margin.right)

		if self.collided_y == Direction.up:
			pyxel.play(3, 21)

		self.__create_animation()

	def __create_animation(self) -> None:
		if not self.is_happy:
			if self.is_falling:
				if self.x_direction == Direction.left:
					self.animate("fall_left", 2)
				elif self.x_direction == Direction.right:
					self.animate("fall_right", 2)
			elif self.is_jumping:
				if self.x_direction == Direction.left:
					self.animate("jump_left", 2)
				elif self.x_direction == Direction.right:
					self.animate("jump_right", 2)
			elif self.is_ground:
				if self.is_walking:
					if self.x_direction == Direction.left:
						self.animate("walk_left", 4)
					elif self.x_direction == Direction.right:
						self.animate("walk_right", 4)
				else:
					if self.x_direction == Direction.left:
						self.animate("idle_left", 5)
					elif self.x_direction == Direction.right:
						self.animate("idle_right", 5)
		else:
			self.animate("happy", 3)
