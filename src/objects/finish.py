from utils.object import Object

class Finish(Object):
	def __init__(self, x, y) -> None:
		super().__init__()

		self.width = 16
		self.height = 16
		self.x = x
		self.y = y
		self.animation_name = "idle"
		self.animations = {
			"idle": [
				[64, 96], [80, 96], [96, 96], [112, 96],
				[64, 112], [80, 112], [96, 112], [112, 112],
			],
		}
		self.tilemap = 0

	def update(self) -> None:
		self.animate("idle", 4)
