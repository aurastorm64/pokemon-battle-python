'''POKeMON BATTLE TEST'''
import random, sys, time


stat_abbreviation = {"ATK":"ATTACK", "DEF":"DEFENSE","SPD":"SPEED","SPC":"SPECIAL","ACC":"ACCURACY","EVS":"EVASION"}


def dialogue(string):
	'''Prints a message one character at a time'''
	for char in string:
		print(char, end="")
		sys.stdout.flush()
		time.sleep(0.05)
	print()

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
					  "DRAGON": ["DRAGON"]}

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
					"DRAGON": []}

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
				 'DRAGON': []}

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


def opponent_move(user, target):
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
		self.movenames = [pkm_data[10], pkm_data[11], pkm_data[12], pkm_data[13]]
		self.level = 5
		self.iv = {"ATK": random.randint(0, 15), "DEF": random.randint(0, 15), "SPD": random.randint(0, 15),"SPC": random.randint(0, 15)}
		self.stat = get_stats(self.basestat, self.level, self.iv)
		self.hp = self.stat["HP"]
		self.statmod = {"ATK":0,"DEF":0,"SPD":0,"SPC":0,"ACC":0,"EVS":0}
		self.move1 = Attack(pkm_data[10])
		self.move2 = Attack(pkm_data[11])
		self.move3 = Attack(pkm_data[12])
		self.move4 = Attack(pkm_data[13])
		
	def attack(self, target, move):
		if accuracy_check(self, target, move):
			dialogue("{} used {}!".format(self.name, move.name))
			if move.category != "STATUS":
				level = self.level
				if crit_check(self):
					dialogue("Critical hit!")
					level = level * 2
				if move.category == "PHYSICAL":
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

				target.hp -= calc_damage
			else:
				if move.target == "TARGET":
					if move.mod < 0:
						if target.statmod[move.targetstat] > -6:
							target.statmod[move.targetstat] += move.mod
							dialogue("{}'s {} fell!".format(target.name, stat_abbreviation[move.targetstat]))
						else:
							dialogue("Nothing happened!")
					else:
						if target.statmod[move.targetstat] < 6:
							target.statmod[move.targetstat] += move.mod
							dialogue("{}'s {} rose!".format(target.name, stat_abbreviation[move.targetstat]))
						else:
							dialogue("Nothing happened!")
				else:
					if move.mod < 0:
						if self.statmod[move.targetstat] > -6:
							self.statmod[move.targetstat] += move.mod
							dialogue("{}'s {} fell!".format(self.name, stat_abbreviation[move.targetstat]))
						else:
							dialogue("Nothing happened!")
					else:
						if self.statmod[move.targetstat] < 6:
							self.statmod[move.targetstat] += move.mod
							dialogue("{}'s {} rose!".format(self.name, stat_abbreviation[move.targetstat]))
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
				
			else:
				self.target = atk_data[3]
				self.targetstat = atk_data[4]
				self.accuracy = int(atk_data[5])
				self.maxpp = int(atk_data[6])
				self.mod = int(atk_data[7])
			self.pp = self.maxpp
		else:
			self.name = None

	def __bool__(self):
		if self.name is None:
			return False
	
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

# BATTLE TEST

print("BULBASAUR, CHARMANDER, SQUIRTLE", end="")
player_choice = input(" >")
opponent = "BLUE"
if player_choice.lower() == "charmander":
	player_pkm = Pokemon(player_choice.lower())
	opponent_pkm = Pokemon("squirtle")
elif player_choice.lower() == "squirtle":
	player_pkm = Pokemon(player_choice.lower())
	opponent_pkm = Pokemon("bulbasaur")
elif player_choice.lower() == "bulbasaur":
	player_pkm = Pokemon(player_choice.lower())
	opponent_pkm = Pokemon("charmander")
elif player_choice.lower() == "dev":
	player_choice = input("What Pokemon do you choose? >")
	player_pkm = Pokemon(player_choice.lower())
	player_choice = input("What Pokemon to battle? >")
	opponent_pkm = Pokemon(player_choice.lower())
else:
	opponent_pkm = Pokemon("eevee")
	player_pkm = Pokemon("pikachu")

dialogue("{} wants to fight!".format(opponent))
dialogue("{} sent out {}!".format(opponent, opponent_pkm.name))
dialogue("Go! {}".format(player_pkm.name))


while True:
	for move in player_pkm.movenames:
		if not move is None:
			print("{} ".format(move), end='')
			sys.stdout.flush()
	player_choice = input(">")
	if player_choice.upper() == player_pkm.move1.name and player_pkm.move1.name:
		player_pkm.attack(opponent_pkm, player_pkm.move1)
	elif player_choice.upper() == player_pkm.move2.name and player_pkm.move2.name:
		player_pkm.attack(opponent_pkm, player_pkm.move2)
	elif player_choice.upper() == player_pkm.move3.name and player_pkm.move3.name:
		player_pkm.attack(opponent_pkm, player_pkm.move3)
	elif player_choice.upper() == player_pkm.move4.name and player_pkm.move4.name:
		player_pkm.attack(opponent_pkm, player_pkm.move4)

	print("{}: {}/{}".format(opponent_pkm.name, opponent_pkm.hp, opponent_pkm.stat["HP"]))

	if opponent_pkm.hp == 0:
		dialogue("{} fainted!".format(opponent_pkm.name))
		dialogue("{} was defeated!".format(opponent))
		break

	opponent_move(opponent_pkm, player_pkm)

	if player_pkm.hp == 0:
		dialogue("{} fainted!".format(player_pkm.name))
		dialogue("PLAYER is out of usable Pokemon!")
		dialogue("PLAYER blacked out!")
		break

	print("{}: {}/{}".format(player_pkm.name, player_pkm.hp, player_pkm.stat["HP"]))



time.sleep(1)





	

	
