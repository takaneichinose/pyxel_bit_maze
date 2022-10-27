from tkinter import N
import pyxel

from utils.scene import Scene
from objects.character import Character
from objects.trap import Trap
from objects.finish import Finish
from utils.utils import Direction

character: Character = None
finish: Finish = None
traps: list[Trap] = []

class GameScene(Scene):
	screen_width: int = 0
	screen_height: int = 0
	game_started: bool = False
	show_instructions: bool = True
	game_over: bool = False
	is_win: bool = None

	def __init__(self, width: int, height: int, fps: int) -> None:
		super().__init__(fps)

		self.screen_width = width
		self.screen_height = height

		self.initialize()
	
	def initialize(self) -> None:
		self.game_started = False
		self.show_instructions = True
		self.game_over = False
		self.is_win = None

		global character
		character = Character(128, 16)

		global traps
		traps.clear()
		traps.append(Trap(128, 48))
		traps.append(Trap(80, 64))
		traps.append(Trap(16, 96))
		traps.append(Trap(48, 160))
		traps.append(Trap(128, 192))

		global finish
		finish = Finish(128, 208)

	def start_game(self) -> None:
		self.game_started = True
		pyxel.playm(1, loop = True)

	def update(self) -> None:
		super().update()

		if not self.game_started:
			self.fade_in(1000, self.start_game)
			return

		if (pyxel.btnp(pyxel.KEY_SPACE) \
		or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)) \
		and character.is_ground:
			if not character.disabled_controls:
				pyxel.play(3, 20)
			elif self.game_over:
				pyxel.play(3, 23)

		self.character_animation()
		self.character_collision()

		finish.update()

	def character_animation(self) -> None:
		if character.is_hurt:
			if character.x_direction == Direction.left:
				character.animate("hurt_left", 5, self.end_game)
			elif character.x_direction == Direction.right:
				character.animate("hurt_right", 5, self.end_game)
		else:
			character.update()

		if self.show_instructions:
			if pyxel.btnp(pyxel.KEY_LEFT) \
			or pyxel.btnp(pyxel.KEY_RIGHT) \
			or pyxel.btnp(pyxel.KEY_SPACE) \
			or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) \
			or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) \
			or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
				self.show_instructions = False

		if self.game_over:
			if pyxel.btnp(pyxel.KEY_SPACE) \
			or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
				self.fade_out(1000, self.restart_game)

	def restart_game(self) -> None:
		self.initialize()

	def character_collision(self) -> None:
		for trap in list(traps):
			trap.update()

			if character.collided(trap):
				if not character.disabled_controls:
					pyxel.stop()
					pyxel.play(3, 22)
				character.dx = 0
				character.disabled_controls = True
				character.is_hurt = True
				trap.is_hidden = False

		if character.collided(finish):
			if not character.disabled_controls:
				pyxel.stop()
				pyxel.play(3, 24)
			character.dx = 0
			character.disabled_controls = True
			character.is_happy = True
			self.game_over = True
			self.is_win = True

	def end_game(self) -> None:
		self.game_over = True
		self.is_win = False

	def draw(self) -> None:
		pyxel.cls(12)

		pyxel.camera()
		pyxel.bltm(0, 0, 1, 0, 0, self.screen_width, self.screen_height, 0)

		half_height = self.screen_height / 2

		scroll_y = 0 if character.y - (half_height) < 0 else character.y - (half_height)
		scroll_y = (half_height) if character.y - (half_height) > (half_height) else scroll_y

		pyxel.camera(0, scroll_y)
		pyxel.bltm(0, 0, 0, 0, scroll_y / 256, 160, 240, 0)

		for trap in list(traps):
			trap.draw()

		finish.draw()
		character.draw()

		pyxel.camera()

		self.draw_text()

	def draw_text(self) -> None:
		if self.show_instructions:
			pyxel.rect(10, 65, 140, 30, 0)
			pyxel.text(14, 69, "Find the finish line", 7)
			pyxel.text(14, 77, "Press LEFT or RIGHT arrow to move", 7)
			pyxel.text(14, 85, "Press SPACE BAR to jump", 7)

		if self.game_over:
			pyxel.rect(10, 65, 140, 30, 0)
			
			if self.is_win:
				pyxel.text(14, 69, "YOU WIN!", 7)
				pyxel.text(14, 77, "You found the mysterious plant!", 7)
			else:
				pyxel.text(14, 69, "YOU LOSE!", 7)
				pyxel.text(14, 77, "You bumped into a mean spider!", 7)

			pyxel.text(14, 85, "Press SPACE BAR to play again", 7)
