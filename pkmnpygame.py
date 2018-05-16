import sys, pygame, pygame.color, textwrap, pkmnpy

def dialogue(string):
	'''Prints a message one character at a time'''

	screen.blit(textbox, [0, 96])
	pygame.display.flip()

	lines = textwrap.fill(string, width=16).splitlines()
	for line_num in range(len(lines)):
		i = 1
		if line_num == 0:
			for char in lines[line_num]:
				if char != ' ':
					screen.blit(font_chars[char], [8*i, 112])
					pygame.display.flip()
				i += 1
				pygame.time.delay(100)
		else:
			if line_num >= 2:
				screen.blit(textbox, [0, 96])
				i = 1
				for char in lines[line_num-2]:
					if char != ' ':
						screen.blit(font_chars[char], [8 * i, 104])
					i += 1

				i = 1
				for char in lines[line_num-1]:
					if char != ' ':
						screen.blit(font_chars[char], [8 * i, 120])
					i += 1

				pygame.display.flip()
				pygame.time.delay(100)
				screen.blit(textbox, [0, 96])

				i = 1
				for char in lines[line_num-1]:
					if char != ' ':
						screen.blit(font_chars[char], [8 * i, 112])
					i += 1
				pygame.display.flip()


			i = 1
			for char in lines[line_num]:
				if char != ' ':
					screen.blit(font_chars[char], [8*i, 128])
					pygame.display.flip()
				i += 1
				pygame.time.delay(100)


		if len(lines) == 1 or (len(lines) > 1 and line_num > 0):
			pygame.event.clear()
			cursor_count = 0
			advance_text = False
			while not advance_text:
				if cursor_count == 50:
					screen.blit(font_chars[" "], [144, 128])
					pygame.display.flip()
				elif cursor_count == 0 or cursor_count == 100:
					screen.blit(cursor_down, [144, 128])
					pygame.display.flip()
					cursor_count = 0
				cursor_count += 1
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
							advance_text = True
				pygame.time.delay(10)

	screen.blit(textbox, [0, 96])
	pygame.display.flip()


def text(string, position):
	'''Outputs text without any special effects. Does not update display.'''
	i = 0
	for char in string:
		if char != ' ':
			screen.blit(font_chars[char], [8 * i + position[0], position[1]])
		i += 1


pygame.init()

pkmnpy.dialogue = dialogue
font_chars = {}
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ!1234567890":
	font_chars[char] = pygame.image.load("img/font/{}.png".format(char))
for char in "abcdefghijklmnopqrstuvwxyz":
	font_chars[char] = pygame.image.load("img/font/{}l.png".format(char))
font_chars[" "] = pygame.image.load("img/font/space.png")
font_chars["."] = pygame.image.load("img/font/period.png")



palette_dark = pygame.color.Color("#204631")
palette_meddark = pygame.color.Color("#527F39")
palette_medlight = pygame.color.Color("#AEC440")
palette_light = pygame.color.Color("#D7E894")

bg_width = 160
bg_height = 144

screen = pygame.display.set_mode([bg_width, bg_height])
screen.fill(palette_light)


battle_select = pygame.image.load("img/battle_01.png")
battle_move_select = pygame.image.load("img/battle_02.png")
battle_intro = pygame.image.load("img/demo_screen.png")
textbox = pygame.image.load("img/textbox_01.png")
cursor_down = pygame.image.load("img/font/cursor_down.png")
cursor_right = pygame.image.load("img/font/cursor_right.png")

screen.blit(battle_intro, [0,0])

pygame.display.flip()

dialogue("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG!")
dialogue("The quick brown fox jumps over the lazy dog.")

text("Press ESCAPE to", [8, 112])
text("close.", [8, 128])
pygame.display.flip()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit()

	pygame.time.delay(10)
