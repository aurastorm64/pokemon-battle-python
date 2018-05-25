'''POKeMON BATTLE TEST'''
import random, sys, time, click, os

if os.name == 'nt':
	is_windows = True
else:
	is_windows = False

if sys.stdout.isatty():
	in_terminal = True
else:
	in_terminal = False

stat_abbreviation = {"ATK":"ATTACK", "DEF":"DEFENSE","SPD":"SPEED","SPC":"SPECIAL","ACC":"ACCURACY","EVS":"EVASION"}
effect_message = {"FRZ":"{} was frozen solid!","BRN":"{} was burned!","PSN":"{} was poisoned!","SLP":"{} fell asleep!","PAR":"{} is paralyzed! It may not attack!"}
effect_message2 = {"FRZ":"frozen","BRN":"burned","PSN":"poisoned","SLP":"asleep","PAR":"paralyzed"}

multiturns = {'SKY ATTACK':'{} is glowing!','SKULL BASH':'{} lowered its head!','SOLARBEAM':'{} took in sunlight!'}
def dialogue(string, auto = False):
	'''Prints a message one character at a time'''
	for char in string:
		if char == "~":
			print("'", end="")
			sys.stdout.flush()
			time.sleep(0.05)
			print("s", end = "")
			time.sleep(0.05)

		else:
			print(char, end="")
			sys.stdout.flush()
			time.sleep(0.05)
			
	print()

def atk_sound(effectiveness):
	'''Used with PyGame version'''
	pass

def deal_damage(target, damage):
	'''Lowers the HP of the Pokemon. The Pygame version overrides this with its own function in order to animate.'''
	target.hp -= damage


def choice_cursor(choices):
	'''Creates a cursor selection from different options'''

	choices_new = []
	for choice in choices:
		if not choice is None:
			choices_new.append(choice)
	selection = 0

	# Apparently the way the cursor selection is done isn't supported in Windows, so if running on Windows, the old selection will be used instead
	if is_windows:
		for choice in choices_new:
			print('{}, '.format(choice), end='')
		print('\b\b ',end='')
		sys.stdout.flush()
		while True:
			selection = input('>')
			if selection in choices_new or selection.lower() == "dev":
				break
			elif selection.lower() == 'quit' or selection.lower() == 'exit':
				print("Exiting.")
				sys.exit()
			elif selection.lower() in ['missingno','missingno.']:
				selection = 'missingno'
				break
			else:
				print("Invalid choice.")
		return selection
		
	
	else:
		while True:
			for i in range(len(choices_new)):
				if i == selection:
					print(">", end='')
				else:
					print(" ", end='')
				print('{}, '.format(choices_new[i]), end='')
			print('\b\b ', end='')
			sys.stdout.flush()

			key = click.getchar()
			if key == "\x1b[D":
				selection = (selection - 1) % len(choices_new)
				print("\r", end="")
			elif key == "\x1b[C":
				selection = (selection + 1) % len(choices_new)
				print("\r", end="")
			elif key == "q":
				print()
				sys.exit()
			elif key == "\x0d":
				break
		print()
		return(choices_new[selection])


def get_pkm(name):
	'''Retrieve Pokemon data such as name, moves, etc. from file'''
	pkm_dat = []
	txtfile = open('pkm/{}.pkm'.format(name.lower()),'r')
	for line in txtfile:
		if line.strip() == "NONE":
			pkm_dat.append(None)
		elif "\t" in line.strip():
			pkm_dat.append(int(line.strip()[-2] + line.strip()[-1]))
		else:
			pkm_dat.append(line.strip())
	txtfile.close()
	return pkm_dat


def moves_for_level(pkm_data, level):
	'''Parse the raw move data from a Pokemon's .pkm file and return the four moves it learned last'''
	moves_parsed = []
	for i in range(10,len(pkm_data)):
		moves_parsed.append(eval(pkm_data[i]))
	moves_up_to_level = []
	for move in moves_parsed:
		if move[1] <= level:
			moves_up_to_level.append(move[0])
	moves_for_level = []
	if len(moves_up_to_level) < 4:
		for i in range(4):
			if i < len(moves_up_to_level):
				moves_for_level.append(moves_up_to_level[i])
			else:
				moves_for_level.append(None)
	else:
		moves_for_level = [moves_up_to_level[-4],moves_up_to_level[-3],moves_up_to_level[-2],moves_up_to_level[-1]]
	return moves_for_level







def get_atk(name):
	'''Retrieve Attack data such as power, accuracy, etc. from file'''
	if name:
		atk_dat = []
	
		txtfile = open('atk/{}.atk'.format(name.lower()),'r')
		for line in txtfile:
			atk_dat.append(line.strip())
		return atk_dat
	
	else:
		return None


def get_matchup(move_type, target_type1, target_type2):
	'''Looks up the type matchup and returns the appropriate damage multiplier'''

	multiplier = 1
	strong_against = {"NORMAL": [],
					  "FIGHTING": ["NORMAL", "ROCK", "ICE"],
					  "FLYING": ["FIGHTING", "BUG", "GRASS"],
					  "POISON": ["BUG", "GRASS"],
					  "GROUND": ["POISON", "ROCK", "FIRE", "ELECTRIC"],
					  "ROCK": ["FLYING", "BUG", "FIRE", "ICE"],
					  "BUG": ["POISON", "GRASS", "PSYCHIC"],
					  "GHOST": ["GHOST"],
					  "FIRE": ["BUG", "GRASS", "ICE"],
					  "WATER": ["GROUND", "ROCK", "FIRE"],
					  "GRASS": ["GROUND", "ROCK", "WATER"],
					  "ELECTRIC": ["FLYING", "WATER"],
					  "PSYCHIC": ["FIGHTING", "POISON"],
					  "ICE": ["FLYING", "GROUND", "GRASS", "DRAGON"],
					  "DRAGON": ["DRAGON"],
					  "BIRD":[]}

	weak_against = {"NORMAL": ["ROCK"],
					"FIGHTING": ["FLYING", "POISON", "BUG", "PSYCHIC"],
					"FLYING": ["ROCK", "ELECTRIC"],
					"POISON": ["POISON", "GROUND", "ROCK", "GHOST"],
					"GROUND": ["BUG", "GRASS"],
					"ROCK": ["FIGHTING", "ROCK"],
					"BUG": ["FIGHTING", "FLYING", "GHOST", "FIRE"],
					"GHOST": [],
					"FIRE": ["ROCK", "FIRE", "WATER", "DRAGON"],
					"WATER": ["WATER", "GRASS", "DRAGON"],
					"GRASS": ["FLYING", "POISON", "BUG", "FIRE", "GRASS", "DRAGON"],
					"ELECTRIC": ["GRASS", "ELECTRIC", "DRAGON"],
					"PSYCHIC": ["PSYCHIC"],
					"ICE": ["WATER", "ICE"],
					"DRAGON": [],
					"BIRD":[]}

	no_effect = {'NORMAL': ['GHOST'],
				 'FIGHTING': ['GHOST'],
				 'FLYING': [],
				 'POISON': [],
				 'GROUND': ['FLYING'],
				 'ROCK': [],
				 'BUG': [],
				 'GHOST': ['NORMAL', 'PSYCHIC'],
				 'FIRE': [],
				 'WATER': [],
				 'GRASS': [],
				 'ELECTRIC': ['GROUND'],
				 'PSYCHIC': [],
				 'ICE': [],
				 'DRAGON': [],
				 'BIRD':[]}

	if target_type1 in strong_against[move_type]:
		multiplier *= 2
	if target_type2 in strong_against[move_type]:
		multiplier *= 2

	if target_type1 in weak_against[move_type]:
		multiplier /= 2
	if target_type2 in weak_against[move_type]:
		multiplier /= 2

	if target_type1 in no_effect[move_type] or target_type2 in no_effect[move_type]:
		multiplier = 0

	if multiplier > 1:
		dialogue("It's super effective!")
	elif multiplier < 1:
		dialogue("It's not very effective...")

	return multiplier


def calculate_stat(base_stat, level, iv, is_hp=False):
	'''Calculate a single Pokemon stat'''
	if not(is_hp):
		calc_stat = (((base_stat + iv)*2)*level//100)+5
	else:
		hp_iv = int((str(iv["ATK"]&1)+str(iv["DEF"]&1)+str(iv["SPD"]&1)+str(iv["SPC"]&1)),2)
		calc_stat = (((base_stat + hp_iv)*2)*level//100)+level+5
	return calc_stat


def get_stats(base_stats, level, iv):
	'''Calculate and return all of a Pokemon's stats'''
	calc_stats = {}
	calc_stats["HP"] = calculate_stat(base_stats["HP"],level,iv,True)
	calc_stats["ATK"] = calculate_stat(base_stats["ATK"],level,iv["ATK"])
	calc_stats["DEF"] = calculate_stat(base_stats["DEF"],level,iv["DEF"])
	calc_stats["SPC"] = calculate_stat(base_stats["SPC"],level,iv["SPC"])
	calc_stats["SPD"] = calculate_stat(base_stats["SPD"],level,iv["SPD"])
	return calc_stats


def calc_statmod(stat, mod):
	'''Calculates the in-battle stats with modifiers'''
	multipliers = {-6:25,-5:28,-4:33,-3:40,-2:50,-1:66,0:100,1:150,2:200,3:250,4:300,5:350,6:400}
	return (stat * (multipliers[mod]/100))


def accuracy_check(user, target, move):
	'''Determine whether or not a move hits'''
	if move.accuracy == "-":
		return True
	else:
		prob_of_hit = int(move.accuracy * ((calc_statmod(100, user.statmod["ACC"]))/(calc_statmod(100, target.statmod["EVS"]*-1))))
		prob_of_hit = prob_of_hit * 2.55
		if prob_of_hit > 255:
			prob_of_hit = 255
		if random.randint(0,255) < prob_of_hit:
			return True
		else:
			return False


def crit_check(user):
	'''Determine whether or not a move lands a critical hit'''
	threshold = user.basestat["SPD"] // 2
	if threshold > 255:
		threshold = 255
	if random.randint(0,255) < threshold:
		return True
	else:
		return False


def probability_check(probability):
	'''Determine whether or not a move's secondary effect activates'''
	if random.randint(0,255) <= probability * 2.55:
		return True
	else:
		return False
		
		
def player_turn(player_pkm):
	can_attack = True
	if player_pkm.status_effect == "FRZ":
		dialogue("{} is frozen solid!".format(player_pkm.name))
		can_attack = False
	elif player_pkm.status_effect == "PAR":
		if probability_check(25):
			dialogue("{} is paralyzed!".format(player_pkm.name))
			can_attack = False
	elif player_pkm.status_effect == "SLP":
		if player_pkm.effect_counter == 0:
			dialogue("{} woke up!".format(player_pkm.name))
			player_pkm.status_effect = None
		else:
			dialogue("{} is fast asleep!".format(player_pkm.name))	
			player_pkm.effect_counter -= 1
		can_attack = False
	elif player_pkm.status_effect == "CON":
		if player_pkm.effect_counter == 0:
			dialogue("{} is no longer confused!".format(player_pkm.name))
			player_pkm.status_effect = None
		else:
			dialogue("{} is confused!".format(player_pkm.name))
			if probability_check(50):
				atk = calc_statmod(player_pkm.stat["ATK"], player_pkm.statmod["ATK"])
				tdef = calc_statmod(player_pkm.stat["DEF"], player_pkm.statmod["DEF"])
				rand = random.randint(217,255)
				calc_damage = int((((((2*player_pkm.level)//5+2)*40*atk//tdef)//50+2)*rand)//255)
				deal_damage(player_pkm, calc_damage)
				dialogue("It attacked itself in its confusion!")
				can_attack = False
	
	if player_pkm.status_effect == "BRN":
		burnt = True
	else:
		burnt = False
		
	if can_attack:
		if player_pkm.multiturn_move != None and player_pkm.multiturn == 1:
			player_pkm.attack(opponent_pkm, player_pkm.multiturn_move, burnt)
			player_pkm.multiturn_move = None
			player_pkm.multiturn = 0
		else:
			player_choice = choice_cursor(player_pkm.movenames)
			if player_choice.upper() == player_pkm.move1.name and player_pkm.move1.name:
				player_pkm.attack(opponent_pkm, player_pkm.move1, burnt)
			elif player_choice.upper() == player_pkm.move2.name and player_pkm.move2.name:
				player_pkm.attack(opponent_pkm, player_pkm.move2, burnt)
			elif player_choice.upper() == player_pkm.move3.name and player_pkm.move3.name:
				player_pkm.attack(opponent_pkm, player_pkm.move3, burnt)
			elif player_choice.upper() == player_pkm.move4.name and player_pkm.move4.name:
				player_pkm.attack(opponent_pkm, player_pkm.move4, burnt)
				
	
		
	
			


def opponent_move(user, target):
	can_attack = True
	if user.status_effect == "FRZ":
		dialogue("{} is frozen solid!".format(user.name))
		can_attack = False
	elif user.status_effect == "PAR":
		if probability_check(25):
			dialogue("{} is paralyzed!".format(user.name))
			can_attack = False
	elif user.status_effect == "SLP":
		if user.effect_counter == 0:
			dialogue("{} woke up!".format(user.name))
			user.status_effect = None
		else:
			dialogue("{} is fast asleep!".format(user.name))	
			user.effect_counter -= 1
		can_attack = False
	elif user.status_effect == "CON":
		if user.effect_counter == 0:
			dialogue("{} is no longer confused!".format(user.name))
			user.status_effect = None
		else:
			dialogue("{} is confused!".format(user.name))
			if probability_check(50):
				atk = calc_statmod(user.stat["ATK"], user.statmod["ATK"])
				tdef = calc_statmod(user.stat["DEF"], user.statmod["DEF"])
				rand = random.randint(217,255)
				calc_damage = int((((((2*user.level)//5+2)*40*atk//tdef)//50+2)*rand)//255)
				deal_damage(user, calc_damage)
				dialogue("It attacked itself in its confusion!")
				can_attack = False
	

	if user.status_effect == "BRN":
		burnt = True
	else:
		burnt = False
	
	if can_attack:
		moves = []
		for move in user.movenames:
			if not move is None:
				moves.append(move)
		opponent_choice = random.choice(moves)
		if opponent_choice == user.move1.name and user.move1.name:
			user.attack(target, user.move1)
		elif opponent_choice == user.move2.name and user.move2.name:
			user.attack(target, user.move2)
		elif opponent_choice == user.move3.name and user.move3.name:
			user.attack(target, user.move3)
		elif opponent_choice == user.move4.name and user.move4.name:
			user.attack(opponent_pkm, user.move4)
			
		


class Pokemon:
	def __init__(self, name):
		pkm_data = get_pkm(name)
					
		self.name = pkm_data[0]
		self.type1 = pkm_data[1]
		self.type2 = pkm_data[2]
		self.basestat = {"HP":pkm_data[4],"ATK":pkm_data[5],"DEF":pkm_data[6],"SPC":pkm_data[7],"SPD":pkm_data[8]}
		self.level = 5
		self.movenames = moves_for_level(pkm_data, self.level)

		self.iv = {"ATK": random.randint(0, 15), "DEF": random.randint(0, 15), "SPD": random.randint(0, 15),"SPC": random.randint(0, 15)}
		self.stat = get_stats(self.basestat, self.level, self.iv)
		self.hp = self.stat["HP"]
		self.statmod = {"ATK":0,"DEF":0,"SPD":0,"SPC":0,"ACC":0,"EVS":0}
		self.move1 = Attack(self.movenames[0])
		self.move2 = Attack(self.movenames[1])
		self.move3 = Attack(self.movenames[2])
		self.move4 = Attack(self.movenames[3])
		self.status_effect = None
		self.effect_counter = 0
		self.multiturn_move = None
		self.multiturn = 0
		self.damage_fx = None
		
	def attack(self, target, move, BRN = False):
		
		if move.status_effect in multiturns and not self.multiturn == 1:
			self.multiturn_move = move
			self.multiturn = 1
			move.pp += 1
			dialogue(multiturns[move.status_effect].format(self.name))
		
		
		elif accuracy_check(self, target, move):
			dialogue("{} used {}!".format(self.name, move.name), True)

			if move.category != "STATUS":
				crit = False
				level = self.level
				if crit_check(self):    
					crit = True
					level = level * 2
				if move.category == "PHYSICAL":
					if BRN:
						atk = calc_statmod(self.stat["ATK"]//2, self.statmod["ATK"])
					else:
						atk = calc_statmod(self.stat["ATK"], self.statmod["ATK"])
					tdef = calc_statmod(target.stat["DEF"], target.statmod["DEF"])
				else:
					atk = calc_statmod(self.stat["SPC"], self.statmod["SPC"])
					tdef = calc_statmod(target.stat["SPC"], target.statmod["SPC"])
				pwr = move.damage
				rand = random.randint(217,255)
				if move.type == self.type1 or move.type == self.type2:
					STAB = 1.5
				else:
					STAB = 1
				type_eff = get_matchup(move.type, target.type1, target.type2)

				calc_damage = int((((((2*level)//5+2)*pwr*atk//tdef)//50+2)*rand)//255*STAB*type_eff)
				atk_sound(type_eff)
				deal_damage(target, calc_damage)
				if crit:
					dialogue("Critical hit!", True)
				if move.status_effect in ['ATK','DEF','SPD','SPC']:
					if probability_check(move.probability):
						if target.statmod[move.status_effect] > -6:
							target.statmod[move.status_effect] -= 1
							dialogue("{}~ {} fell!".format(target.name, stat_abbreviation[move.status_effect]))
				elif move.status_effect in ['BRN','PAR','SLP','PSN','FRZ']:
					if probability_check(move.probability):
						if target.status_effect == move.status_effect:
							dialogue("{} is already {}!".format(target.name, effect_message2[move.status_effect]))
						else:
							target.status_effect = move.status_effect
							dialogue(effect_message[move.status_effect].format(target.name))
							if move.status_effect == "SLP":
								target.effect_counter = random.randint(1,7)
							elif move.status_effect == "CON":
								target.effect_counter = random.randint(1,4)
				elif move.status_effect not in ["NONE","SOLARBEAM","SKULL BASH","SKY ATTACK"]:
					print("This move's mechanics have not been implemented yet")

			else:
				if move.name == 'LEECH SEED':
					if target.type1 == 'GRASS' or target.type2 == 'GRASS':
						dialogue("It doesn't affect {}".format(target.name))
					else:
						dialogue("{} was seeded!".format(target.name))
						target.damage_fx = 'LEECH SEED'
				elif move.name == 'SLEEP POWDER':
					target.status_effect = "SLP"
					target.effect_counter = random.randint(1,7)
					dialogue("{} fell asleep!".format(target.name))
				else:
					if move.target == "TARGET":
						if move.mod < 0:
							if target.statmod[move.targetstat] > -6:
								target.statmod[move.targetstat] += move.mod
								dialogue("{}~ {} fell!".format(target.name, stat_abbreviation[move.targetstat]))
							else:
								dialogue("Nothing happened!")
						else:
							if target.statmod[move.targetstat] < 6:
								target.statmod[move.targetstat] += move.mod
								dialogue("{}~ {} rose!".format(target.name, stat_abbreviation[move.targetstat]))
							else:
								dialogue("Nothing happened!")
					else:
						if move.mod < 0:
							if self.statmod[move.targetstat] > -6:
								self.statmod[move.targetstat] += move.mod
								dialogue("{}~ {} fell!".format(self.name, stat_abbreviation[move.targetstat]))
							else:
								dialogue("Nothing happened!")
						else:
							if self.statmod[move.targetstat] < 6:
								self.statmod[move.targetstat] += move.mod
								dialogue("{}~ {} rose!".format(self.name, stat_abbreviation[move.targetstat]))
							else:
								dialogue("Nothing happened!")
		else:
			dialogue("The attack missed!")
		move.pp -= 1
		if self.hp < 0:
			self.hp = 0
		if target.hp < 0:
			target.hp = 0
		
					
class Attack:
	def __init__(self, name):
		atk_data = get_atk(name)
		if atk_data:
			self.name = atk_data[0]
			self.category = atk_data[1]
			self.type = atk_data[2]
			if self.category != "STATUS":
				self.damage = int(atk_data[3])
				self.accuracy = int(atk_data[4])
				self.maxpp = int(atk_data[5])
				self.status_effect = atk_data[6]
				if self.status_effect != "NONE":
					self.probability = int(atk_data[7])

				
			else:
				self.target = atk_data[3]
				self.targetstat = atk_data[4]
				self.status_effect = None
				if atk_data[5] == "-":
					self.accuracy = "-"
				else:
					self.accuracy = int(atk_data[5])
				self.maxpp = int(atk_data[6])
				if self.targetstat == "STATUS":
					self.mod = atk_data[7]
				else:
					self.mod = int(atk_data[7])
					
			self.pp = self.maxpp
		else:
			self.name = None

	def __bool__(self):
		if self.name is None:
			return False


class Trainer:
	def __init__(self, name, t_class="TRAINER"):
		self.name = name
		self.team = []
		self.t_class = t_class
		self.active_slot = 0
	
'''
charmander = Pokemon("charmander")
print(charmander.name)
print(charmander.move1.name)

squirtle = Pokemon("squirtle")
print(squirtle.name)
print(squirtle.hp)

charmander.attack(squirtle, charmander.move1)

print(squirtle.hp)

print(charmander.statmod["DEF"])
squirtle.attack(charmander, squirtle.move2)

print(charmander.statmod["DEF"])
'''
if __name__ == "__main__":
	# BATTLE TEST

	# Setup battle
	player = Trainer("RED")
	opponent = Trainer("BLUE","RIVAL")

	
	player_choice = choice_cursor(['BULBASAUR','CHARMANDER','SQUIRTLE', 'PIKACHU'])
	
	if player_choice.lower() == "charmander":
		player.team.append(Pokemon(player_choice.lower()))
		opponent.team.append(Pokemon("squirtle"))
	elif player_choice.lower() == "squirtle":
		player.team.append(Pokemon(player_choice.lower()))
		opponent.team.append(Pokemon("bulbasaur"))
	elif player_choice.lower() == "bulbasaur":
		player.team.append(Pokemon(player_choice.lower()))
		opponent.team.append(Pokemon("charmander"))
	elif player_choice.lower() == "dev":
		player_choice = input("What Pokemon do you choose? >")
		player.team.append(Pokemon(player_choice.lower()))
		player_choice = input("What Pokemon to battle? >")
		opponent.team.append(Pokemon(player_choice.lower()))
	else:
		opponent.team.append(Pokemon("eevee"))
		if player_choice.lower() == "missingno." or player_choice.lower() == 'missingno':
			player.team.append(Pokemon("missingno"))
		else:
			player.team.append(Pokemon("pikachu"))

	player_pkm = player.team[player.active_slot]
	opponent_pkm = opponent.team[opponent.active_slot]

	dialogue("{} wants to fight!".format(opponent.name))
	dialogue("{} sent out {}!".format(opponent.name, opponent_pkm.name))
	dialogue("Go! {}".format(player_pkm.name))


	# Main turn loop
	while True:
		
		player_turn(player_pkm)

		print("{}: {}/{}".format(opponent_pkm.name, opponent_pkm.hp, opponent_pkm.stat["HP"]))
		
		if player_pkm.status_effect == "PSN" and opponent_pkm.hp != 0:
			dialogue("{} is hurt by poison!".format(player_pkm.name))
			deal_damage(player_pkm, player_pkm.stat["HP"]//16)
		elif player_pkm.status_effect == "BRN" and opponent_pkm.hp != 0:
			dialogue("{} is hurt by the burn!".format(player_pkm.name))
			deal_damage(player_pkm, player_pkm.stat["HP"] // 16)
			
		if player_pkm.damage_fx == "LEECH SEED":
			dialogue("LEECH SEED saps {}!".format(player_pkm.name))
			deal_damage(player_pkm, player_pkm.stat["HP"] // 16)
		
			
			
		if opponent_pkm.hp == 0:
			dialogue("{} fainted!".format(opponent_pkm.name))
			dialogue("{} was defeated!".format(opponent.name))
			break

		opponent_move(opponent_pkm, player_pkm)
		
		if opponent_pkm.status_effect == "PSN" and player_pkm.hp != 0:
			dialogue("{} is hurt by poison!".format(opponent_pkm.name))
			deal_damage(opponent_pkm, opponent_pkm.stat["HP"] // 16)
		elif opponent_pkm.status_effect == "BRN" and player_pkm.hp != 0:
			dialogue("{} is hurt by the burn!".format(opponent_pkm.name))
			deal_damage(opponent_pkm, opponent_pkm.stat["HP"] // 16)

		if opponent_pkm.damage_fx == "LEECH SEED":
			dialogue("LEECH SEED saps {}".format(opponent_pkm.name))
			deal_damage(opponent_pkm, opponent_pkm.stat["HP"] // 16)
			
			
		if player_pkm.hp == 0:
			dialogue("{} fainted!".format(player_pkm.name))
			dialogue("{} is out of usable Pokemon!".format(player.name))
			dialogue("{} blacked out!".format(player.name))
			break

		print("{}: {}/{}".format(player_pkm.name, player_pkm.hp, player_pkm.stat["HP"]))



	time.sleep(1)





	

	
