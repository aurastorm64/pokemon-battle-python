import sys, pygame, pygame.color, textwrap, pkmnpy

# The keys that are used as the A button on a GameBoy
a_keys = [pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER]


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
				pygame.time.delay(50)
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
				pygame.time.delay(50)
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
				pygame.time.delay(50)


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
						if event.key in a_keys:
							advance_text = True
				pygame.time.delay(10)

	screen.blit(textbox, [0, 96])
	pygame.display.flip()

def dialogue_auto(string):
	'''dialoogue function, but it doesn't require the user to press any button to advance'''
	screen.blit(textbox, [0, 96])
	pygame.display.flip()

	lines = textwrap.fill(string, width=16).splitlines()
	for line_num in range(len(lines)):
		i = 1
		if line_num == 0:
			for char in lines[line_num]:
				if char != ' ':
					screen.blit(font_chars[char], [8 * i, 112])
					pygame.display.flip()
				i += 1
				pygame.time.delay(50)
		else:
			if line_num >= 2:
				screen.blit(textbox, [0, 96])
				i = 1
				for char in lines[line_num - 2]:
					if char != ' ':
						screen.blit(font_chars[char], [8 * i, 104])
					i += 1

				i = 1
				for char in lines[line_num - 1]:
					if char != ' ':
						screen.blit(font_chars[char], [8 * i, 120])
					i += 1

				pygame.display.flip()
				pygame.time.delay(50)
				screen.blit(textbox, [0, 96])

				i = 1
				for char in lines[line_num - 1]:
					if char != ' ':
						screen.blit(font_chars[char], [8 * i, 112])
					i += 1
				pygame.display.flip()

			i = 1
			for char in lines[line_num]:
				if char != ' ':
					screen.blit(font_chars[char], [8 * i, 128])
					pygame.display.flip()
				i += 1
				pygame.time.delay(50)

def text(string, position):
	'''Outputs text without any special effects. Does not update display.'''
	i = 0
	for char in string:
		if char != ' ':
			screen.blit(font_chars[char], [8 * i + position[0], position[1]])
		i += 1


def draw_hp(target):
	if target == "PLAYER":
		pygame.draw.rect(screen, palette_light, [96,75,48,2],0)
		bar_width = int(48 * (player_pkm.hp / player_pkm.stat["HP"]))
		pygame.draw.rect(screen, palette_dark, [96, 75, bar_width, 2],0)
		pygame.draw.rect(screen, palette_light, [88, 80, 24, 8],0)
		text(str(player_pkm.hp).rjust(3), [88, 80])

	else:
		pygame.draw.rect(screen, palette_light, [32, 19, 48, 2],0)
		bar_width = int(48 * (opponent_pkm.hp / opponent_pkm.stat["HP"]))
		pygame.draw.rect(screen, palette_dark, [32,19,bar_width,2],0)


def deal_damage(target, damage):
	'''Lowers the HP of the Pokemon and animates the damage bar.'''
	old_hp = target.hp
	old_bar = int(48 * (target.hp / target.stat["HP"]))
	target.hp -= damage
	if target.hp < 0:
		target.hp = 0
	new_bar = int(48 * (target.hp / target.stat["HP"]))


	if target == player_pkm:
		for i in range(10):
			if i % 2 == 0:
				pygame.draw.rect(screen, palette_light, [4, 32, 64, 64], 0)
			else:
				screen.blit(player_pkm.sprite, [2, 32])
			pygame.display.flip()
			pygame.time.delay(100)
			
		for i in range(old_bar - new_bar):
			pygame.draw.rect(screen, palette_light, [96, 75, 48, 2], 0)
			pygame.draw.rect(screen, palette_dark, [96, 75, old_bar-i, 2], 0)
			pygame.draw.rect(screen, palette_light, [88, 80, 24, 8], 0)
			text(str(player_pkm.hp).rjust(3), [88, 80])
			pygame.display.flip()
			pygame.time.delay(500//(old_hp - target.hp))
	else:
		for i in range(10):
			if i % 2 == 0:
				pygame.draw.rect(screen, palette_light, [94, 0, 64, 56], 0)
			else:
				screen.blit(opponent_pkm.sprite, [94, 0])
			pygame.display.flip()
			pygame.time.delay(100)
			
		for i in range(old_bar - new_bar):
			pygame.draw.rect(screen, palette_light, [32, 19, 48, 2], 0)
			pygame.draw.rect(screen, palette_dark, [32, 19, old_bar-i, 2], 0)
			pygame.display.flip()
			pygame.time.delay(500//(old_hp - target.hp))



def animate_intro(player, opponent):
	screen.blit(textbox, [0, 96])
	pygame.display.flip()
	for i in range(4, 80):
		pygame.draw.rect(screen, palette_light, [0, 0, 160, 96], 0)
		screen.blit(opponent.sprite, [i*2-64, 0])
		screen.blit(player.sprite, [160-i*2, 32])
		pygame.display.flip()
		pygame.time.delay(20)
	screen.blit(pokeball_bar, [74, 80])
	screen.blit(pokeball_bar2, [8, 8])
	pygame.display.flip()
	
	dialogue("{} wants to fight!".format(opponent.name))
	
	pygame.draw.rect(screen, palette_light, [0, 0, 160, 96], 0)
	screen.blit(player.sprite, [2, 32])
	screen.blit(opponent.sprite, [94, 0])
	pygame.display.flip()
	
	for i in range(0, 18):
		pygame.draw.rect(screen, palette_light, [0, 0, 160, 96], 0)
		screen.blit(opponent.sprite, [94+i*4, 0])
		screen.blit(player.sprite, [2, 32])
		pygame.display.flip()
		pygame.time.delay(10)

	dialogue_auto("{} sent out {}!".format(opponent.name, opponent_pkm.name))
	pygame.time.delay(250)
	screen.blit(opponent_pkm.sprite, [94, 0])
	pygame.display.flip()
	pygame.time.delay(250)
	screen.blit(opponent_hud, [0,0])
	text(opponent_pkm.name, [8,0])
	text(str(opponent_pkm.level), [40,8])
	draw_hp("OPPONENT")
	pygame.display.flip()
	pygame.time.delay(250)

	for i in range(0, 18):
		pygame.draw.rect(screen, palette_light, [0, 32, 72, 64], 0)
		screen.blit(player.sprite, [2-i*4, 32])
		pygame.display.flip()
		pygame.time.delay(10)

	dialogue_auto("Go! {}!".format(player_pkm.name))
	screen.blit(player_hud, [0,0])
	text(player_pkm.name, [80,56])
	text(str(player_pkm.level), [120,64])
	text(str(player_pkm.hp).rjust(3), [88,80])
	text(str(player_pkm.stat["HP"]).rjust(3), [120,80])
	draw_hp("PLAYER")
	pygame.display.flip()
	pygame.time.delay(250)
	screen.blit(player_pkm.sprite, [2,32])
	pygame.display.flip()
	pygame.time.delay(250)


	
	
pkmnpy.dialogue = dialogue
pkmnpy.deal_damage = deal_damage
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
pokeball_bar = pygame.image.load("img/pokeballs.png")
pokeball_bar2 = pygame.image.load("img/pokeballs_opponent.png")
opponent_hud = pygame.image.load("img/opponent_hud.png")
player_hud = pygame.image.load("img/player_hud.png")

'''
screen.blit(battle_intro, [0,0])

pygame.display.flip()


dialogue("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG!")
dialogue("The quick brown fox jumps over the lazy dog.")
'''

player = pkmnpy.Trainer("RED")
opponent = pkmnpy.Trainer("BLUE", "RIVAL")
player.sprite = pygame.image.load("img/player.png")
opponent.sprite = pygame.image.load("img/rival.png")

player.team.append(pkmnpy.Pokemon("charmander"))
opponent.team.append(pkmnpy.Pokemon("squirtle"))

player_pkm = player.team[player.active_slot]
opponent_pkm = opponent.team[opponent.active_slot]
player_pkm.sprite = pygame.image.load("img/pkm/back/{}.png".format(player_pkm.name))
opponent_pkm.sprite = pygame.image.load("img/pkm/front/{}.png".format(opponent_pkm.name))


animate_intro(player, opponent)


player_pkm.attack(opponent_pkm, player_pkm.move1)


opponent_pkm.attack(player_pkm, opponent_pkm.move1)



screen.blit(textbox, [0, 96])
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
