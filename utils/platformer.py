import pyxel

from utils.object import Object
from utils.utils import Direction

class Platformer(Object):
	tilemap: list = None
	tile_width: int = 8
	tile_height: int = 8
	acceleration: float = 0.1
	max_dx: float = 2
	deceleration: float = 0.85
	gravity: float = 0.2
	jump_speed: float = 4
	max_dy: float = 4
	bounce: float = 0
	x_direction: Direction = None
	y_direction: Direction = None
	is_walking: bool = False
	is_jumping: bool = False
	is_falling: bool = False
	is_ground: bool = True
	solid_tilemap: int = 0
	solid_list: list = None
	disabled_controls: bool = False
	collided_x: int = None
	collided_y: int = None

	def __init__(self) -> None:
		super(Platformer, self).__init__()

	def update(self) -> None:
		self.__update_x()
		self.__update_y()

	def __check_solid(self, direction) -> bool:
		if direction == Direction.up:
			x1 = self.x + self.margin.left
			x2 = self.x + self.width - self.margin.right - 1
			y1 = self.y + self.margin.top
			y2 = self.y + self.margin.top + 1
		elif direction == Direction.down:
			x1 = self.x + self.margin.left
			x2 = self.x + self.width - self.margin.right - 1
			y1 = self.y + self.height - self.margin.bottom - 1
			y2 = self.y + self.height - self.margin.bottom
		elif direction == Direction.left:
			x1 = self.x + self.margin.left
			x2 = self.x + self.margin.left + 1
			y1 = self.y + self.margin.top
			y2 = self.y + self.height - self.margin.bottom - 1
		elif direction == Direction.right:
			x1 = self.x + self.width - self.margin.right - 1
			x2 = self.x + self.width - self.margin.right
			y1 = self.y + self.margin.top
			y2 = self.y + self.height - self.margin.bottom - 1
		else:
			return

		tilemap: pyxel.Tilemap = pyxel.tilemap(self.solid_tilemap)

		for tile in self.solid_list:
			if tilemap.pget(pyxel.floor(x1 / 8), pyxel.floor(y1 / 8)) == tile \
			or tilemap.pget(pyxel.floor(x1 / 8), pyxel.floor(y2 / 8)) == tile \
			or tilemap.pget(pyxel.floor(x2 / 8), pyxel.floor(y1 / 8)) == tile \
			or tilemap.pget(pyxel.floor(x2 / 8), pyxel.floor(y2 / 8)) == tile :
				return True

		return False

	def __update_x(self) -> None:
		if (pyxel.btn(pyxel.KEY_LEFT) \
		or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)) \
		and not self.disabled_controls:
			self.dx -= self.acceleration
			self.x_direction = Direction.left
			self.is_walking = True
		elif (pyxel.btn(pyxel.KEY_RIGHT) \
		or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)) \
		and not self.disabled_controls:
			self.dx += self.acceleration
			self.x_direction = Direction.right
			self.is_walking = True
		else:
			self.dx *= self.deceleration

		if self.dx >= self.max_dx:
			self.dx = self.max_dx
		elif self.dx <= -self.max_dx:
			self.dx = -self.max_dx

		if abs(self.dx) <= 0.01:
			self.dx = 0
		elif abs(self.dx) <= 0.1:
			self.is_walking = False

		self.x += self.dx
		self.collided_x = None
		dx_direction = Direction.left if self.dx < 0 else Direction.right

		if self.__check_solid(dx_direction):
			self.dx = 0
			self.collided_x = self.x_direction
			tile_width = pyxel.floor(self.x / self.tile_width) * self.tile_width
			
			if dx_direction == Direction.left:
				self.x = tile_width + self.tile_width - self.margin.left
			elif dx_direction == Direction.right:
				self.x = tile_width + self.margin.right

	def __update_y(self) -> None:
		self.dy += self.gravity

		if (pyxel.btnp(pyxel.KEY_SPACE) \
		or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)) \
		and self.is_ground \
		and not self.disabled_controls:
			self.dy = -self.jump_speed
			self.is_ground = False

		if self.dy > self.max_dy:
			self.dy = self.max_dy
		elif self.dy < -self.max_dy:
			self.dy = -self.max_dy

		self.y += self.dy

		if self.dy < 0:
			self.y_direction = Direction.up
		elif self.dy > 0:
			self.y_direction = Direction.down

		self.collided_y = None

		if self.__check_solid(self.y_direction):
			self.dy = self.dy * -self.bounce if self.y_direction == Direction.down else 0
			if abs(self.dy) <= 0.1:
				self.dy = 0
			tile_height = pyxel.floor(self.y / self.tile_height) * self.tile_height

			if self.y_direction == Direction.up:
				self.y = tile_height + self.tile_height - self.margin.top
			elif self.y_direction == Direction.down:
				self.y = tile_height + self.margin.bottom

			self.collided_y = self.y_direction
		
		self.is_jumping = not self.is_ground and self.dy < 0
		self.is_falling = not self.is_ground and self.dy > 0
		self.is_ground = self.dy == 0
