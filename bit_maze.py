import pyxel

from scenes.game_scene import GameScene

SCREEN_WIDTH: int = 160
SCREEN_HEIGHT: int = 160
FPS: int = 30

game_scene: GameScene = None

class App:
	def __init__(self) -> None:
		pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, "Bit Maze", FPS)
		pyxel.load("assets/bit_maze.pyxres")

		global game_scene
		game_scene = GameScene(SCREEN_WIDTH, SCREEN_HEIGHT, FPS)

		pyxel.run(self.update, self.draw)

	def update(self) -> None:
		game_scene.update()

	def draw(self) -> None:
		game_scene.draw()

App()
