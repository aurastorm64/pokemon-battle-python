'''POKeMON BATTLE TEST'''
import random

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
	#TODO: Add this
	return 1


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
	multipliers = {-6:25,-5:28,-4:33,-2:50,-1:66,0:100,1:150,2:200,3:250,4:300,5:350,6:400}
	return (stat * (multipliers[mod]/100))
	
def accuracy_check(user, target, move):
	prob_of_hit = int(move.accuracy * ((calc_statmod(100, user.accmod["ACC"]))/(calc_statmod(100, user.accmod["EVS"]*-1))))
	prob_of_hit = prob_of_hit * 2.55
	if prob_of_hit > 255:
		prob_of_hit = 255
	if random.randint(0,255) < prob_of_hit:
		return True
	else:
		return False
	
	
class Pokemon:
	def __init__(self, name):
		pkm_data = get_pkm(name)
					
		self.name = pkm_data[0]
		self.type1 = pkm_data[1]
		self.type2 = pkm_data[2]
		self.basestat = {"HP":pkm_data[4],"ATK":pkm_data[5],"DEF":pkm_data[6],"SPC":pkm_data[7],"SPD":pkm_data[8]}
		self.movenames = [pkm_data[10], pkm_data[11], pkm_data[12], pkm_data[13]]
		self.level = 5
		self.iv = {"ATK":15,"DEF":15,"SPD":15,"SPC":15}
		self.stat = get_stats(self.basestat, self.level, self.iv)
		self.hp = self.stat["HP"]
		self.accmod = {"ACC":0,"EVS":0}
		self.statmod = {"ATK":0,"DEF":0,"SPD":0,"SPC":0}
		self.move1 = Attack(pkm_data[10])
		self.move2 = Attack(pkm_data[11])
		self.move3 = Attack(pkm_data[12])
		self.move4 = Attack(pkm_data[13])
		
	def attack(self, target, move):
		if accuracy_check(self, target, move):
			level = self.level
			if move.category == "PHYSICAL":
				atk = self.stat["ATK"]
				tdef = target.stat["DEF"]
			else:
				atk = self.stat["SPC"]
				tdef = target.stat["SPC"]
			pwr = move.damage
			rand = random.randint(217,255)
			if move.type == self.type1 or move.type == self.type2:
				STAB = 1.5
			else:
				STAB = 1
			type_eff = get_matchup(move.type, target.type1, target.type2)
			
			calc_damage = int((((((2*level)//5+2)*pwr*atk//tdef)//50+2)*rand)//255*STAB*type_eff)
			
			target.hp -= calc_damage
			print("{} used {}!".format(self.name, move.name))
		else:
			print("The attack missed!")
		
					
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
			self.pp = self.maxpp
		else:
			return None
			

	

charmander = Pokemon("charmander")
print(charmander.name)
print(charmander.move1.name)

squirtle = Pokemon("squirtle")
print(squirtle.name)
print(squirtle.hp)

charmander.attack(squirtle, charmander.move1)

print(squirtle.hp)

input()



		
	
	

	
