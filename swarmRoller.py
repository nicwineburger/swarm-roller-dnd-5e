# Kean Freeman 2017

import pdb
import dice
import sys
from math import floor

# class definitions
"""
print 'Swarm name? (examples: "Goblin", "Druid")'
print 'Swarm attack bonus? (examples: "+5", "-1", "+0")'
print 'Swarm dice? (examples: "1d6+2", "20d7-1", "5d6+3")'
print 'Hit Points per swarm individual? (examples: "7", "500")'
print 'Number of members of swarm? (examples: "2", "100")'
"""
class Swarm(object):
	def __init__(self, name, attackBonus, damageDice, hitPoints, size):
		self.name = name
		self.attackBonus = attackBonus
		self.damageDice = damageDice
		self.individualHP = hitPoints
		self.size = size

		self.totalHP = self.individualHP * size
		self.currentHP = self.totalHP
		self.currentNumMembers = size

	def inflictDamage(self, damage):
		self.currentHP -= damage
		numDead = floor((self.totalHP - self.currentHP) / self.individualHP)
		self.currentNumMembers =self.size - int(numDead)

# function definitions
def optionsPrompt():
	print 'Input desired action:'
	print '"1": the swarm attacks'
	print '"2": the swarm takes damage'
	print '"q": quit'

def collectSwarmFromFile(fileName):
	print 'Collecting swarm info from ' + fileName + ':'
	with open(fileName) as f:
		fileList = f.read().splitlines()
		if len(fileList) < 5:
			print 'Error: not enough information in creature swarm input file'
			exit(1)

		name = fileList[0]
		print 'Swarm name is "' + name + '"'
		
		attackBonus = 0
		attackBonus += int(fileList[1])
		print 'Swarm attack bonus is: ' + str(attackBonus)

		damageDice = ""
		damageDice = fileList[2]
		print 'Swarm dice are: ' + damageDice

		hitPoints = 0
		hitPoints += int(fileList[3])
		print 'Hit Points per swarm individual: ' + str(hitPoints)
		
		size = 0
		size += int(fileList[4])
		print 'Number of members of swarm: ' + str(size) + '\n'

		return Swarm(name, attackBonus, damageDice, hitPoints, size)

def swarmAttack(swarmIn):
	print 'AC of target? (examples: "5", "20")'
	targetAC = int(raw_input())

	damage = 0
	# dice info below for calculations
	endOfDiceType = (swarmIn.damageDice).find('+')
	diceType = swarmIn.damageDice[:endOfDiceType]
	diceDamageModifier = int(swarmIn.damageDice[endOfDiceType + 1:])
	
	for i in range(swarmIn.currentNumMembers):
		attackRoll = dice.roll('1d20t') + swarmIn.attackBonus
		
		# critical hits always hit, and deal twice the damage dice
		if (attackRoll - swarmIn.attackBonus) == 20:
			dCharPosition = diceType.find('d')
			numDice = int(diceType[:dCharPosition])
			numDice *= 2
			tempDiceType = str(numDice) + diceType[dCharPosition:]
			rollTotal = dice.roll(tempDiceType + 't') + diceDamageModifier
			damage += rollTotal

		elif attackRoll >= targetAC:
			rollTotal = dice.roll(diceType + 't') + diceDamageModifier
			damage += rollTotal
	# TODO: calculating average damage as well for convenience
	"""
	numDice = diceType[:diceType.find('d')]
	diceShape = diceType[diceType.find('d') + 1:]
	averageDamageRoll = float(int(diceShape)/ float(2)) * int(numDice) + \
diceDamageModifier
	numberNeededToHit = targetAC - swarmIn.attackBonus
	chanceOfHitting = float((20 - numberNeededToHit) / float(20))
	
	print 'Approximate average damage: ' + \
str(int((chanceOfHitting * averageDamageRoll) * swarmIn.currentNumMembers))
	"""	

	print 'The swarm deals ' + str(damage) + 'HP damage to the target!\n'
		

def swarmTakesDamage(swarmIn):
	print 'How much HP damage does the swarm take?'
	damageTaken = int(raw_input())
	swarmIn.inflictDamage(damageTaken)
	if swarmIn.currentHP < 0:
		print 'The swarm has no more HP!'
	else:
		print 'After damage, the swarm has ' + str(swarmIn.currentHP) + \
' HP out of ' + str(swarmIn.totalHP) + 'HP!\nAlso, the swarm has ' + \
str(swarmIn.currentNumMembers) + ' member(s) remaining!\n'

# main
if len(sys.argv) != 2:
	print 'Error, need to input monster file name as argument'
	exit(1)
swarm1 = collectSwarmFromFile(sys.argv[1])

while True:
	optionsPrompt()    
	input = raw_input()
	if input == '1':
		swarmAttack(swarm1)
	elif input == '2':
		swarmTakesDamage(swarm1)
	elif (input == 'q'):
		print 'Program terminating'
		exit()
	else:
		print 'Invalid option selected\n'

	