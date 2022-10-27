import pyxel

from typing import Callable
from utils.utils import Margin

class Object:
	width: int = None
	height: int = None
	x: float = 0
	y: float = 0
	dx: float = 0
	dy: float = 0
	margin: Margin = Margin()
	animation_id: int = 1
	animation_name: str = None
	animation_time: int = 0
	animations: dict = None
	is_hidden: bool = False

	def __init__(self) -> None:
		super(Object, self).__init__()

		self.animation_time = pyxel.frame_count

	def draw(self) -> None:
		if self.is_hidden \
		or self.animation_name == None:
			return

		image = self.animations[self.animation_name][self.animation_id]
		u = image[0]
		v = image[1]

		pyxel.blt(self.x, self.y, 0, u, v, self.width, self.height, 0)

	def animate(self, name: str, frames: int, callback: Callable = None) -> None:
		if self.animation_name == None:
			return
		
		if self.animation_name != name:
			self.animation_id = 1
			self.animation_name = name
			self.animation_time = pyxel.frame_count

		elapsed_frame = pyxel.frame_count - self.animation_time

		if elapsed_frame < frames:
			return

		self.animation_time = pyxel.frame_count
		self.animation_id += 1

		end_animation_id = len(self.animations[name]) - 1

		if self.animation_id >= end_animation_id:
			if callback != None:
				self.animation_id = end_animation_id
				callback()
			else:
				self.animation_id = 1

	def collided(self, object) -> bool:
		a_x1 = self.x + self.margin.left
		a_x2 = self.x + self.width - self.margin.right
		a_y1 = self.y + self.margin.top
		a_y2 = self.y + self.height - self.margin.bottom
		b_x1 = object.x + object.margin.left
		b_x2 = object.x + object.width - object.margin.right
		b_y1 = object.y + object.margin.top
		b_y2 = object.y + object.height - object.margin.bottom

		condition_x1 = a_x1 <= b_x1 and a_x2 >= b_x1 and a_x2 <= b_x2
		condition_x2 = a_x1 >= b_x1 and a_x1 <= b_x2 and a_x2 >= b_x2
		condition_x3 = a_x1 >= b_x1 and a_x1 <= b_x2 and a_x2 <= b_x2
		condition_y1 = a_y1 <= b_y1 and a_y2 >= b_y1 and a_y2 <= b_y2
		condition_y2 = a_y1 >= b_y1 and a_y1 <= b_y2 and a_y2 >= b_y2
		condition_y3 = a_y1 >= b_y1 and a_y1 <= b_y2 and a_y2 <= b_y2

		if (condition_x1 and condition_y1) \
		or (condition_x1 and condition_y2) \
		or (condition_x2 and condition_y1) \
		or (condition_x2 and condition_y2) \
		or (condition_x3 and condition_y3):
			return True
		else:
			return False
