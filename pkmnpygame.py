import sys, pygame, pygame.color, textwrap, pkmnpy

# The keys that are used as the A button on a GameBoy
a_keys = [pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER]
b_keys = [pygame.K_BACKSPACE]


def dialogue(string, auto = False):
	'''Prints a message one character at a time'''
	if auto:
		dialogue_auto(string)
	else:

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
					checkfor_mus()
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

							if event.key == pygame.K_ESCAPE:
								sys.exit()
							if event.key in a_keys:
								cmus_sfx.play(sfx_cursor)
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
	pygame.time.delay(250)

def text(string, position):
	'''Outputs text without any special effects. Does not update display.'''
	i = 0
	for char in string:
		if char != ' ':
			screen.blit(font_chars[char], [8 * i + position[0], position[1]])
		i += 1

def atk_sound(effectiveness):
	if effectiveness < 1:
		cmus_sfx.play(sfx_weakhit)
	elif effectiveness > 1:
		cmus_sfx.play(sfx_stronghit)
	else:
		cmus_sfx.play(sfx_normalhit)

def draw_hp(target):
	if target == "PLAYER":
		pygame.draw.rect(screen, palette_light, [96,75,48,2],0)
		if player_pkm.hp != 0:
			bar_width = int(48 * (player_pkm.hp / player_pkm.stat["HP"]))
			pygame.draw.rect(screen, palette_dark, [96, 75, bar_width, 2],0)
		pygame.draw.rect(screen, palette_light, [88, 80, 24, 8],0)
		text(str(player_pkm.hp).rjust(3), [88, 80])

	else:
		pygame.draw.rect(screen, palette_light, [32, 19, 48, 2],0)
		if opponent_pkm.hp != 0:
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
			checkfor_mus()
			pygame.draw.rect(screen, palette_light, [96, 75, 48, 2], 0)
			pygame.draw.rect(screen, palette_dark, [96, 75, old_bar-i, 2], 0)
			pygame.draw.rect(screen, palette_light, [88, 80, 24, 8], 0)
			text(str(int(old_hp - ((old_hp - player_pkm.hp)/(old_bar-new_bar)*i))).rjust(3), [88, 80])
			pygame.display.flip()
			pygame.time.delay(500//(old_hp - target.hp))
		if int(48 * (player_pkm.hp / player_pkm.stat["HP"])) < 10 and player_pkm.hp != 0:
			cmus_pulse.set_volume(0)
			cmus_beep.play(sfx_lowhealth, loops = -1)
		else:
			cmus_beep.stop()
			cmus_pulse.set_volume(0.50)
	else:
		for i in range(10):
			checkfor_mus()
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
	cmus_main.set_volume(0)
	cmus_sfx.play(opponent_pkm.cry)
	cmus_main.set_volume(0.50)
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
	cmus_main.set_volume(0)
	cmus_sfx.play(player_pkm.cry)
	cmus_main.set_volume(0.50)
	screen.blit(player_pkm.sprite, [2,32])
	pygame.display.flip()
	pygame.time.delay(250)

def checkfor_mus():
	if not cmus_main.get_busy():
		cmus_main.play(mus_main, loops = -1)
		cmus_pulse.play(mus_pulse, loops = -1)

def menu(menu_type, cursor_start = [0,0]):
	'''Handles the menu selection'''
	global move_cursor

	if menu_type == "MAIN":
		cursor_pos = cursor_start
		screen.blit(textbox_battlemenu, [0, 96])
		pygame.draw.rect(screen, palette_light, [72, 112, 8, 8], 0)
		screen.blit(cursor_right, [(72 + cursor_pos[0]*48), (112 + cursor_pos[1]*16)])
		pygame.display.flip()
		selecting = True
		while selecting:
			checkfor_mus()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					pygame.draw.rect(screen, palette_light, [(72 + cursor_pos[0]*48), (112 + cursor_pos[1]*16), 8, 8], 0)
					if event.key == pygame.K_ESCAPE:
						sys.exit()
					elif event.key in a_keys:
						cmus_sfx.play(sfx_cursor)
						if cursor_pos[0] + cursor_pos[1] == 2:
							if battle_type == "TRAINER":
								pygame.draw.rect(screen, palette_light, [0, 96, 160, 48], 0)
								dialogue("No! There~ no running from a trainer battle!") # '~' is used for apostrophe s
								screen.blit(textbox_battlemenu, [0, 96])
								pygame.draw.rect(screen, palette_light, [72, 112, 8, 8], 0)
								pygame.display.flip()
							else:
								choice = "RUN"
								selecting = False
								break
						elif cursor_pos[0] + cursor_pos[1] == 0:
							selecting = False
							choice = "FIGHT"
							break
						elif cursor_pos[0] == 0 and cursor_pos[1] == 1:
							choice = "ITEM"
							selecting = False
							break
						else:
							pygame.draw.rect(screen, palette_light, [0, 96, 160, 48], 0)
							dialogue("POKéMON menu not implemented yet.")
							
							screen.blit(textbox_battlemenu, [0, 96])
							pygame.draw.rect(screen, palette_light, [72, 112, 8, 8], 0)
							pygame.display.flip()

					elif event.key == pygame.K_LEFT:
						cursor_pos[0] = 0
					elif event.key == pygame.K_RIGHT:
						cursor_pos[0] = 1
					elif event.key == pygame.K_UP:
						cursor_pos[1] = 0
					elif event.key == pygame.K_DOWN:
						cursor_pos[1] = 1
					screen.blit(cursor_right, [(72 + cursor_pos[0]*48), (112 + cursor_pos[1]*16)])
					pygame.display.flip()
		pygame.draw.rect(screen, palette_light, [0, 96, 160, 48], 0)


	elif menu_type == "FIGHT":
		num_of_moves = 0
		for move in [player_pkm.move1, player_pkm.move2, player_pkm.move3, player_pkm.move4]:
			if not move.name is None:
				num_of_moves += 1


		screen.blit(textbox_fight, [0,0])
		pygame.draw.rect(screen, palette_light, [40, 104, 8, 8], 0)
		if player_pkm.move1.name is not None:
			pygame.draw.rect(screen, palette_light, [48, 104, 8, 8], 0)
			text(player_pkm.move1.name, [48, 104])
		if player_pkm.move2.name is not None:
			pygame.draw.rect(screen, palette_light, [48, 112, 8, 8], 0)
			text(player_pkm.move2.name, [48, 112])
		if player_pkm.move3.name is not None:
			pygame.draw.rect(screen, palette_light, [48, 120, 8, 8], 0)
			text(player_pkm.move3.name, [48, 120])
		if player_pkm.move4.name is not None:
			pygame.draw.rect(screen, palette_light, [48, 128, 8, 8], 0)
			text(player_pkm.move4.name, [48, 128])
			pygame.draw.rect(screen, palette_light, [40, 104, 8, 8], 0)

		if move_cursor == 0:
			current_move = player_pkm.move1
		elif move_cursor == 1:
			current_move = player_pkm.move2
		elif move_cursor == 2:
			current_move = player_pkm.move3
		else:
			current_move = player_pkm.move4

		screen.blit(textbox_type, [0, 64])
		screen.blit(cursor_right, [40, 104 + (move_cursor * 8)])
		text(current_move.type, [16, 80])
		text(str(current_move.pp).rjust(2), [40, 88])
		text(str(current_move.maxpp).rjust(2), [64, 88])

		pygame.display.flip()
		selecting = True

		while selecting:
			checkfor_mus()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					pygame.draw.rect(screen, palette_light, [40, 104+(8*move_cursor), 8, 8], 0)
					if event.key == pygame.K_ESCAPE:
						sys.exit()
					elif event.key in a_keys:
						cmus_sfx.play(sfx_cursor)
						if current_move.pp == 0:
							dialogue("No PP left for this move!")
						choice = move_cursor
						selecting = False
						break
					elif event.key in b_keys:
						cmus_sfx.play(sfx_cursor)
						choice = "BACK"
						selecting = False
						break
					elif event.key == pygame.K_UP:
						move_cursor = (move_cursor - 1) % num_of_moves
					elif event.key == pygame.K_DOWN:
						move_cursor = (move_cursor + 1) % num_of_moves


					if move_cursor == 0:
						current_move = player_pkm.move1
					elif move_cursor == 1:
						current_move = player_pkm.move2
					elif move_cursor == 2:
						current_move = player_pkm.move3
					else:
						current_move = player_pkm.move4

					screen.blit(textbox_type, [0,64])
					text(current_move.type, [16, 80])
					text(str(current_move.pp).rjust(2), [40,88])
					text(str(current_move.maxpp).rjust(2), [64, 88])
					screen.blit(cursor_right, [40, 104+(move_cursor*8)])
					pygame.display.flip()

		pygame.draw.rect(screen, palette_light, [0, 96, 160, 48], 0)
		pygame.draw.rect(screen, palette_light, [0, 64, 88, 40], 0)
		screen.blit(player_pkm.sprite, [2, 32])
		screen.blit(player_hud, [0,0])
		text(player_pkm.name, [80,56])
		text(str(player_pkm.level), [120,64])
		text(str(player_pkm.hp).rjust(3), [88,80])
		text(str(player_pkm.stat["HP"]).rjust(3), [120,80])
		draw_hp("PLAYER")

	elif menu_type == "ITEM":
		screen.blit(textbox, [0,96])
		screen.blit(textbox_item, [0, 0])
		
		pygame.display.flip()
		selecting = True
		while selecting:
			checkfor_mus()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						sys.exit()
					elif event.key in a_keys:
						cmus_sfx.play(sfx_cursor)
						choice = "BACK"
						selecting = False
						break
					elif event.key in b_keys:
						cmus_sfx.play(sfx_cursor)
						choice = "BACK"
						selecting = False
						break
		screen.fill(palette_light)
		screen.blit(opponent_hud, [0,0])
		screen.blit(opponent_pkm.sprite, [94, 0])
		text(opponent_pkm.name, [8,0])
		text(str(opponent_pkm.level), [40,8])
		draw_hp("OPPONENT")
		screen.blit(player_hud, [0,0])
		text(player_pkm.name, [80,56])
		text(str(player_pkm.level), [120,64])
		text(str(player_pkm.hp).rjust(3), [88,80])
		text(str(player_pkm.stat["HP"]).rjust(3), [120,80])
		draw_hp("PLAYER")
		screen.blit(player_pkm.sprite, [2,32])
		
	elif menu_type == "SETUP":
		text("Choose a POKeMON!", [8, 8])
		text("BULBASAUR", [16, 24])
		text("CHARMANDER", [16, 32])
		text("SQUIRTLE", [16, 40])
		text("PIKACHU", [16, 48])
		cursor_pos = 1
		choices = ["missingno","bulbasaur", "charmander", "squirtle", "pikachu"]
		screen.blit(cursor_right, [8, 16+(cursor_pos*8)])
		pygame.display.flip()
		selecting = True
		while selecting:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						sys.exit()
					elif event.key == pygame.K_UP:
						pygame.draw.rect(screen, palette_light, [8, 16+(cursor_pos*8), 8, 8], 0)
						if cursor_pos == 1:
							cursor_pos = 0
						elif cursor_pos == 0:
							cursor_pos = 4
						else:
							cursor_pos = ((cursor_pos - 1)-1) % 4 + 1
						screen.blit(cursor_right, [8, 16+(cursor_pos*8)])
						pygame.display.flip()
					elif event.key == pygame.K_DOWN:
						pygame.draw.rect(screen, palette_light, [8, 16+(cursor_pos*8), 8, 8], 0)
						cursor_pos = ((cursor_pos + 1)-1) % 4 + 1
						screen.blit(cursor_right, [8, 16+(cursor_pos*8)])
						pygame.display.flip()
					
					elif event.key in a_keys:
						cmus_sfx.play(sfx_cursor)
						choice = choices[cursor_pos]
						selecting = False
						break
					
			
			
	return choice

def animate_fainted(target):
	if target == "OPPONENT":
		for i in range(18):
			pygame.draw.rect(screen, palette_light, [94, 0, 64, 72], 0)
			screen.blit(opponent_pkm.sprite, [94, i*4])
			pygame.draw.rect(screen, palette_light, [72, 56, 64, 88], 0)
			pygame.draw.rect(screen, palette_light, [0, 96, 160, 48], 0)
			screen.blit(player_hud, [0, 0])
			text(player_pkm.name, [80, 56])
			text(str(player_pkm.level), [120, 64])
			text(str(player_pkm.hp).rjust(3), [88, 80])
			text(str(player_pkm.stat["HP"]).rjust(3), [120, 80])
			draw_hp("PLAYER")
			screen.blit(textbox, [0, 96])
			lines = textwrap.fill("{} fainted!".format(opponent_pkm.name), width=16).splitlines()
			text(lines[0], [8, 112])
			if len(lines) > 1:
				text(lines[1], [8, 128])
			pygame.display.flip()
			pygame.time.delay(10)
		pygame.draw.rect(screen, palette_light, [0, 0, 96, 32], 0)
		pygame.display.flip()
	else:
		for i in range(18):
			pygame.draw.rect(screen, palette_light, [0, 32, 64, 64], 0)
			screen.blit(player_pkm.sprite, [2, 32+i*4])
			pygame.draw.rect(screen, palette_light, [0, 96, 160, 48], 0)
			screen.blit(textbox, [0, 96])
			lines = textwrap.fill("{} fainted!".format(player_pkm.name), width=16).splitlines()
			text(lines[0], [8, 112])
			if len(lines) > 1:
				text(lines[1], [8, 128])
			pygame.display.flip()
			pygame.time.delay(10)


def blackout():
	cmus_sfx.stop()
	cmus_pulse.stop()
	cmus_beep.stop()
	cmus_main.stop()
	for color in [palette_medlight, palette_meddark, palette_dark]:
		screen.fill(color)
		pygame.display.flip()
		pygame.time.delay(100)
	pygame.time.delay(500)

def rival_defeat():
	cmus_sfx.stop()
	cmus_pulse.set_volume(0)
	cmus_beep.stop()
	cmus_main.set_volume(0)
	cmus_beep.play(mus_victory)
	dialogue("{} defeated {}!".format(player.name, opponent.name))
	for i in range(0, 18):
		pygame.draw.rect(screen, palette_light, [0, 0, 160, 96], 0)
		screen.blit(opponent.sprite, [160-i*4, 0])
		screen.blit(player_pkm.sprite, [2, 32])

		screen.blit(player_hud, [0, 0])
		text(player_pkm.name, [80, 56])
		text(str(player_pkm.level), [120, 64])
		text(str(player_pkm.hp).rjust(3), [88, 80])
		text(str(player_pkm.stat["HP"]).rjust(3), [120, 80])
		draw_hp("PLAYER")
		pygame.display.flip()
		pygame.time.delay(10)

	dialogue("{}: WHAT? Unbelievable! I picked the wrong POKéMON!".format(opponent.name))



# POKEMON BATTLE PYGAME
pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.mixer.init()
pygame.init()

# Override pkmnpy's functions with version for PyGame
pkmnpy.dialogue = dialogue
pkmnpy.deal_damage = deal_damage
pkmnpy.atk_sound = atk_sound

font_chars = {}
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ!-1234567890é":
	font_chars[char] = pygame.image.load("img/font/{}.png".format(char))
for char in "abcdefghijklmnopqrstuvwxyz":
	font_chars[char] = pygame.image.load("img/font/{}l.png".format(char))
font_chars[" "] = pygame.image.load("img/font/space.png")
font_chars["."] = pygame.image.load("img/font/period.png")
font_chars["~"] = pygame.image.load("img/font/apos_s.png")
font_chars[":"] = pygame.image.load("img/font/colon.png")
font_chars["?"] = pygame.image.load("img/font/question.png")



palette_dark = pygame.color.Color("#204631")
palette_meddark = pygame.color.Color("#527F39")
palette_medlight = pygame.color.Color("#AEC440")
palette_light = pygame.color.Color("#D7E894")

bg_width = 160
bg_height = 144

screen = pygame.display.set_mode([bg_width, bg_height])
screen.fill(palette_light)

# IMAGES
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
textbox_battlemenu = pygame.image.load("img/textbox_02.png")
textbox_fight = pygame.image.load("img/textbox_fight.png")
textbox_type = pygame.image.load("img/textbox_type.png")
textbox_item = pygame.image.load("img/textbox_item.png")

# MUSIC
cmus_main = pygame.mixer.Channel(0)
cmus_pulse = pygame.mixer.Channel(1)
cmus_sfx = pygame.mixer.Channel(2)
cmus_beep = pygame.mixer.Channel(3)

cmus_main.set_volume(0.50)
cmus_pulse.set_volume(0.50)
cmus_sfx.set_volume(0.50)
cmus_beep.set_volume(0.50)

mus_intro = pygame.mixer.Sound("mus/trainer_intro.wav")
mus_main = pygame.mixer.Sound("mus/trainer_battle_main.wav")
mus_pulse = pygame.mixer.Sound("mus/trainer_battle_pulse.wav")
mus_victory = pygame.mixer.Sound("mus/defeated.wav")
sfx_cursor = pygame.mixer.Sound("sfx/cursor.wav")
sfx_lowhealth = pygame.mixer.Sound("sfx/low_health.wav")
sfx_weakhit = pygame.mixer.Sound("sfx/weakhit.wav")
sfx_normalhit = pygame.mixer.Sound("sfx/normalhit.wav")
sfx_stronghit = pygame.mixer.Sound("sfx/stronghit.wav")


move_cursor = 0 # The cursor remains on the last selected move in the actual game
mainmenu_cursor = [0, 0]
'''
screen.blit(battle_intro, [0,0])

pygame.display.flip()


dialogue("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG!")
dialogue("The quick brown fox jumps over the lazy dog.")
'''

#Get Player's choice of Pokemon
pygame.display.flip()
player_choice = menu("SETUP")


battle_type = "TRAINER"

player = pkmnpy.Trainer("RED")
opponent = pkmnpy.Trainer("BLUE", "RIVAL")
player.sprite = pygame.image.load("img/player.png")
opponent.sprite = pygame.image.load("img/rival.png")

rival_matchup = {"charmander":"squirtle","bulbasaur":"charmander","squirtle":"bulbasaur","pikachu":"eevee","missingno":"eevee"}
if player_choice == "missingno":
	player.team.append(pkmnpy.Pokemon(player_choice, 137))
else:
	player.team.append(pkmnpy.Pokemon(player_choice))
opponent.team.append(pkmnpy.Pokemon(rival_matchup[player_choice]))

player_pkm = player.team[player.active_slot]
opponent_pkm = opponent.team[opponent.active_slot]
if player_pkm.name == "MISSINGNO.":
	player_pkm.sprite = pygame.image.load("img/pkm/back/missingno.png")
else:
	player_pkm.sprite = pygame.image.load("img/pkm/back/{}.png".format(player_pkm.name.lower()))
opponent_pkm.sprite = pygame.image.load("img/pkm/front/{}.png".format(opponent_pkm.name.lower()))
if player_pkm.name != "MISSINGNO.":
	player_pkm.cry = pygame.mixer.Sound("sfx/cry/{}.wav".format(player_pkm.name.lower()))
else:
	player_pkm.cry = pygame.mixer.Sound("sfx/cry/missingno.wav")
opponent_pkm.cry = pygame.mixer.Sound("sfx/cry/{}.wav".format(opponent_pkm.name.lower()))



cmus_main.play(mus_intro)

for i in range(10):
	screen.fill(palette_dark)
	pygame.display.flip()
	pygame.time.delay(50)
	screen.fill(palette_meddark)
	pygame.display.flip()
	pygame.time.delay(50)
	screen.fill(palette_medlight)
	pygame.display.flip()
	pygame.time.delay(50)
	screen.fill(palette_light)
	pygame.display.flip()
	pygame.time.delay(50)
	screen.fill(palette_medlight)
	pygame.display.flip()
	pygame.time.delay(50)
	screen.fill(palette_meddark)
	pygame.display.flip()
	pygame.time.delay(50)
	
screen.fill(palette_light)
pygame.display.flip()
	
animate_intro(player, opponent)

# BATTLE
while True:
	checkfor_mus()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit()

	if player_pkm.multiturn_move is not None:
		menu_sel = 9

	else:
		in_menu = True
		while in_menu:
			checkfor_mus()
			menu_sel = menu("MAIN", mainmenu_cursor)
			if menu_sel == "FIGHT":
				mainmenu_cursor = [0,0]
				menu_sel = menu("FIGHT")
				if menu_sel != "BACK":
					in_menu = False
			elif menu_sel == "ITEM":
				menu_sel = menu("ITEM")
				mainmenu_cursor = [0,1]
				if menu_sel != "BACK":
					in_menu = False


	if pkmnpy.calc_statmod(player_pkm.stat["SPD"], player_pkm.statmod["SPD"]) >= pkmnpy.calc_statmod(opponent_pkm.stat["SPD"], opponent_pkm.statmod["SPD"]):
		if	menu_sel == 0:
			player_pkm.attack(opponent_pkm, player_pkm.move1)
		elif menu_sel == 1:
			player_pkm.attack(opponent_pkm, player_pkm.move2)
		elif menu_sel == 2:
			player_pkm.attack(opponent_pkm, player_pkm.move3)
		elif menu_sel == 3:
			player_pkm,attack(opponent_pkm, player_pkm.move4)
		elif menu_sel == 9:
			player_pkm.attack(opponent_pkm, player_pkm.multiturn_move)
			player_pkm.multiturn_move = None
			player_pkm.multiturn = 0

		if opponent_pkm.hp == 0:
			dialogue("{} fainted!".format(opponent_pkm.name))
			animate_fainted("OPPONENT")
			rival_defeat()
			blackout()
			break

		pkmnpy.opponent_move(opponent_pkm, player_pkm)

	else:
		pkmnpy.opponent_move(opponent_pkm, player_pkm)

		if player_pkm.hp == 0:
			dialogue("{} fainted!".format(player_pkm.name))
			animate_fainted("PLAYER")
			dialogue("{} is out of usable POKéMON!".format(player.name))
			dialogue_auto("{} blacked out!".format(player.name))
			blackout()
			break

		if menu_sel == 0:
			player_pkm.attack(opponent_pkm, player_pkm.move1)
		elif menu_sel == 1:
			player_pkm.attack(opponent_pkm, player_pkm.move2)
		elif menu_sel == 2:
			player_pkm.attack(opponent_pkm, player_pkm.move3)
		elif menu_sel == 3:
			player_pkm, attack(opponent_pkm, player_pkm.move4)
		elif menu_sel == 9:
			player_pkm.attack(opponent_pkm, player_pkm.multiturn_move)
			player_pkm.multiturn_move = None
			player_pkm.multiturn = 0

	if opponent_pkm.hp == 0:
		dialogue("{} fainted!".format(opponent_pkm.name))
		animate_fainted("OPPONENT")
		rival_defeat()
		blackout()
		break

	if player_pkm.hp == 0:
		dialogue("{} fainted!".format(player_pkm.name))
		animate_fainted("PLAYER")
		dialogue("{} is out of usable POKéMON!".format(player.name))
		dialogue_auto("{} blacked out!".format(player.name))
		blackout()
		break





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
