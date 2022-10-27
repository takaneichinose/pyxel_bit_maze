from utils.object import Object

class Trap(Object):
	def __init__(self, x, y) -> None:
		super().__init__()

		self.width = 16
		self.height = 16
		self.x = x
		self.y = y
		self.animation_name = "idle"
		self.animations = {
			"idle": [[64, 80], [80, 80], [96, 80], [112, 80], [96, 80], [80, 80]],
		}
		self.tilemap = 0
		self.is_hidden = True

	def update(self) -> None:
		self.animate("idle", 4)
