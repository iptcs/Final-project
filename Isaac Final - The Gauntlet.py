# The Gauntlet of Power

#This is the class we use to create all the characters in the game. Every action a character can take is stored here
class character:
    def __init__(self, name):
        self.name = name
        self.attributes = {
            "Strength" : 1,
            "Agility" : 1,
            "Vitality" : 1,
            "Knowledge" : 1
            } # Attributes are the baseline values that combat stats are based on. They are stored in a dictionary. The player can
                # increase them directly, unlike combat stats

        #These are the values that the combat methods usually draw from. They function as equations that mix and match attributes
        self.Attack = self.attributes["Strength"] + self.attributes["Agility"]  #How much damage basic attacks deal
        self.DefensePoints = self.attributes["Knowledge"] + 9 #Somewhat like HP. This is how much damage you can take before you start getting wounds, which are what actually kill you
        self.DPRecovery = self.attributes["Agility"] #This determines how much DP you gain when you use the 'defend' method. Note that it is based on a different stat than your max DP
        self.MaxDP = self.attributes["Knowledge"] + 9 #This is the cap for your DP. We use this value to reset the number if it ever gets too high
        self.WoundThreshold = self.attributes["Vitality"] + self.attributes["Strength"] #Strength is what determines how many wounds you get when you are hit with no DP to protect you. This is how many it takes to kill you
        self.Wounds = 0 #Current Wounds
        self.ActionPoints = self.attributes["Agility"] + 1 #These are what allow you to take action during a turn. The turn_cycle function ends your turn when they hit 0
        self.APRecovery = self.attributes["Vitality"] + 1 #Same relationship as that between DP and DPRecovery. Though this regenerates on its own
        self.MaxAP = self.attributes["Agility"] + 2 #Works almost identically to MaxDP
        self.Mana = self.attributes["Vitality"] + self.attributes["Knowledge"] + 3 #This is used to cast spells; abilities you learn from fallen enemies
        self.MaxMana = self.attributes["Vitality"] + self.attributes["Knowledge"] + 3
        self.possible_actions = ["ATTACK" , "DEFEND", "WAIT"] #This list regulates what the player can and cannot do. Since all abilities are part of the class, we need something to limit them and differentiate characters
        self.tactics = [] #This empty list is where each NPC's move pattern will go, where the enemy_turn method cycles through them

    def attack(self, target): #The basic attack function. Note that the Strength attribute determines wounds dealt. We also make sure to reset DP and AP to keep them within limits
        import random
        damage = random.randint(1, 3) + self.Attack
        target.DefensePoints -= damage
        self.ActionPoints -= 1
        print(self.name, " attacks ", target.name, ", dealing ", damage, " damage...")
        if target.DefensePoints <= 0:
            target.DefensePoints = 0
            target.Wounds += self.attributes["Strength"]
            print("And inflicting a serious wound! ", target.name, " now has ", target.Wounds, " wounds")
        if self.ActionPoints < 0:
                self.ActionPoints = 0

    def defend(self): #This restores DP when used
        import random
        defense = random.randint(1, 3) + self.DPRecovery
        self.DefensePoints += defense
        self.ActionPoints -= 1
        print(self.name, " refocuses their guard, regaining ", defense, " defense points")
        if self.ActionPoints < 0:
                self.ActionPoints = 0

    def wait(self, opponent): #This is what allows the PLAYER to wait. The reason this is seperate from the enemy_wait function is because enemy actions and player functions are different, and the wait function needs to call them
        print(self.name, "elects to wait")
        self.recover_AP()
        opponent.enemy_action(self)

    def enemy_wait(self, opponent):
        print(self.name, "elects to wait")
        self.recover_AP()
        opponent.player_action(self)

    def recover_AP(self): #The characters never deliberately call this function. It's a quick way to increase AP at the end of turns and prevent it from going over the limit
        self.ActionPoints =+ self.APRecovery
        if self.ActionPoints > self.MaxAP:
            self.ActionPoints = self.MaxAP
            print(self.name, " has reached maximum AP!")

    def display_actions(self): #This function is used to show the player their options
        print(self.name, " may perform the following: ")
        print(self.possible_actions, "\n")

    def display_combat_stats(self): #This shows character status
        print("\n", self.name, " status:")
        print(self.name, " - Defense Points: ", self.DefensePoints)
        print(self.name, " - Action Points: ", self.ActionPoints)
        print(self.name, " - Wounds: ", self.Wounds)
        print(self.name, " - Mana: ", self.Mana, "\n")

    def player_action(self, opponent): #Takes input from the player so they can make moves. Note that the player is not allowed to use actions they haven't unlocked
        self.display_actions
        print("What will you do? \n")
        action = input("").upper()
        print(action)
        while action not in self.possible_actions:
            print("You must select from your possible actions")
            action = input("").upper()
        if action == "ATTACK":
            self.attack(opponent)
        if action == "DEFEND":
            self.defend()
        if action == "WAIT":
            self.wait(opponent)
        if action == "STOP TIME":
            self.time_stop()
        if action == "UNHOLY RAGE":
            self.unholy_rage(opponent)
        if action == "MEND FLESH":
            self.mend_flesh()
        if action == "SUMMON DEATH":
            self.summon_death(opponent)
        if action == "HEX":
            self.hex(opponent)
        if action == "BATTLE ZEN":
            self.battle_zen()

    def enemy_action(self, opponent): #This is what allows the enemy to act and loop through their tactics
        action = self.tactics[0] #We begin by recording the first action on the tactics list
        self.tactics.append(self.tactics[0]) #Next, we add a copy of that move to the end of the tactics list
        self.tactics.remove(self.tactics[0]) #And remove the orginal, thus creating a cycle
        if action == "ATTACK":
            self.attack(opponent)
        if action == "DEFEND":
            self.defend()
        if action == "WAIT":
            self.enemy_wait(opponent)
        if action == "STOP TIME":
            self.time_stop()
        if action == "UNHOLY RAGE":
            self.unholy_rage(opponent)
        if action == "MEND FLESH":
            self.mend_flesh()
        if action == "SUMMON DEATH":
            self.summon_death(opponent)
        if action == "HEX":
            self.hex(opponent)
        if action == "BATTLE ZEN":
            self.battle_zen()

    def reset_default_stats(self): #We use this function to both heal at the end of fights and also adjust combat stats when attributes change
        self.Attack = self.attributes["Strength"] + self.attributes["Agility"]
        self.DefensePoints = self.attributes["Knowledge"] + 9
        self.DPRecovery = self.attributes["Agility"]
        self.MaxDP = self.attributes["Knowledge"] + 9
        self.WoundThreshold = self.attributes["Vitality"] + self.attributes["Strength"]
        self.Wounds = 0
        self.ActionPoints = self.attributes["Agility"] + 1
        self.APRecovery = self.attributes["Vitality"] + 1
        self.MaxAP = self.attributes["Agility"] + 2
        self.Mana = self.attributes["Vitality"] + self.attributes["Knowledge"] + 3
        self.MaxMana = self.attributes["Vitality"] + self.attributes["Knowledge"] + 3

    def time_stop(self): #A special attack that 'stops time' by giving you a bunch of action points, and thus a lot of moves
        print(self.name, " reaches forth to grab the reigns of fate itself!")
        self.Mana -= 10
        if self.Mana >= 0:
            self.ActionPoints = self.MaxAP * 2
            print("The very fabric of time lays still before them!")
        else:
            print("But they lack the magical might to cast such a monumental spell")
            self.ActionPoints -= 1
            if self.ActionPoints < 0:
                self.ActionPoints = 0

    def summon_death(self, target): #This kills your enemy instantly by making their Wounds and WoundThreshold values equal...
        print(self.name, " speaks tones in a forgotten tongue, to summon eldest of beings")
        self.Mana -= 5
        self.ActionPoints -= 1
        if self.ActionPoints < 0:
                self.ActionPoints = 0
        if self.Mana >= 0:
            import random
            result = random.randint(1, 3)
            if result != 3:
                print("Shadows twist and converge, and a tall, hooded figure emerges from their collective darkness")
                print("The shadowy figure moves faster than thought, and wraps its skeletel hand around the neck of", target.name)
                print("Their soul is condemned to oblivion...")
                target.WoundThreshold = target.Wounds
            if result == 3: #But it can also hurt you
                print("Shadows twist and converge, and a tall, hooded figure emerges from their collective darkness")
                print("The shadow turns its gaze upon the one who summoned it! It lunges with a shriek and grabs a shred of their spirit")
                print(self.name, "has been punished for their hubris; they will bear this mark for the rest of their days")
                self.WoundThreshold -= 1
        else:
            print("The being does not respond")

    def unholy_rage(self, target): #Essentially a more powerful version of 'attack'
        print(self.name, " attempts to conjure the powers of darkness to empower The Red Sword")
        self.Mana -= 2
        self.ActionPoints -= 1
        if self.ActionPoints < 0:
                self.ActionPoints = 0
        if self.Mana >= 0:
            import random
            damage = random.randint(1, 3) + self.Attack + self.MaxMana
            target.DefensePoints -= damage
            self.ActionPoints -= 1
            print(self.name, " infuses their blade with the corrosive energies of dark magic, and smites", target.name, ", dealing ", damage, " damage...")
            if target.DefensePoints <= 0:
                target.DefensePoints = 0
                target.Wounds += self.attributes["Strength"] + self.MaxMana
                print("Unholy magic infests ", target.name, ", causing their injuries to fester; they now have ", target.Wounds, " wounds")
        else:
            print(self.name, " lacks the Mana to cast the spell")

    def mend_flesh(self): #Reduces the user's wound threshold
        print(self.name, " calls upon mystical energies to heal their injuries")
        self.Mana -= 2
        self.ActionPoints -= 1
        if self.ActionPoints < 0:
                self.ActionPoints = 0
        if self.Mana >= 0:
            self.Wounds =- 1
            if self.Wounds < 0:
                self.Wounds = 0
            print(self.name, " weaves an arcane seal, and their wounds begin to close...")
        else:
            print(self.name, " lacks the magical energy to complete the spell")

    def battle_zen(self): #Gives the user a defense boost and a bonus to recovery
        print(self.name, " focuses their breathing, gaining superhuman awareness")
        self.Mana -= 4
        self.ActionPoints -= 1
        if self.ActionPoints < 0:
                self.ActionPoints = 0
        if self.Mana >= 0:
            self.MaxDP += 5
            self.DefensePoints += self.MaxDP
            self.DPRecovery += 1
            print(self.name, " is unnaturally calm. Their composure will make them harder to hit")
        else:
            print(self.name, " lacks the magical energy to complete the spell")

    def hex(self, target): #A magical super attack. Sort of like Unholy Rage, but drawn entirely from Knowledge
        print(self.name, " gathers arcane energies and prepares to release them in a malefic blast")
        self.Mana -= 4
        self.ActionPoints -= 1
        if self.ActionPoints < 0:
                self.ActionPoints = 0
        if self.Mana > 0:
            damage = self.attributes["Knowledge"] * 3
            target.DefensePoints -= damage
            print(target.name, " is assaulted by the wave of violent magic...")
            if target.DefensePoints <= 0:
                target.DefensePoints = 0
                print(" And the magic has inflicted a major wound!")
                target.Wounds += self.attributes["Knowledge"]
        else:
            print("But their magical energies are too drained to contain the power")


def character_creation(character): # This function takes a character and allows the player to modify them
    print("""
Welcome to The Gauntlet of Power

First you must distribute your attribute points. You have three to start with, and each attribute has a default score of 1.
Choose carefully.
""")
    a_points = 3
    while a_points > 0:
        print("You have ", a_points, "attribute points remaining")
        selection = int(input("""Select an attribute to increase
1: Strength - Strength increases the effectiveness of your attacks, and makes you harder to kill
2: Agility - Agility plays a roll in attacking, defensive moves, and how many actions you can take in a turn
3: Vitality - Vitality makes you tougher in every respect; it also means you recover faster, giving you more actions
4: Knowledge - Knowledge helps you defend yourself. It also increases your reserves of mana, which eventually lets you use spells

"""))
        if selection == 1:
            character.attributes["Strength"] += 1
            a_points -= 1
        elif selection == 2:
            character.attributes["Agility"] += 1
            a_points -= 1
        elif selection == 3:
            character.attributes["Vitality"] += 1
            a_points -= 1
        elif selection == 4:
            character.attributes["Knowledge"] += 1
            a_points -= 1
        else:
            print("Input a number between 1 and 4")
    return character

def level_up(character): #Truncated version of character_creation for the purposes of leveling up
    print("""
Your power has increased...
""")
    a_points = 3
    while a_points > 0:
        print("You have ", a_points, "attribute points to spend")
        selection = int(input("""Select an attribute to increase
1: Strength - Strength increases the effectiveness of your attacks, and makes you harder to kill
2: Agility - Agility plays a roll in attacking, defensive moves, and how many actions you can take in a turn
3: Vitality - Vitality makes you tougher in every respect; it also means you recover faster, giving you more actions
4: Knowledge - Knowledge helps you defend yourself. It also increases your reserves of mana, which eventually lets you use spells

"""))
        if selection == 1:
            character.attributes["Strength"] += 1
            a_points -= 1
        elif selection == 2:
            character.attributes["Agility"] += 1
            a_points -= 1
        elif selection == 3:
            character.attributes["Vitality"] += 1
            a_points -= 1
        elif selection == 4:
            character.attributes["Knowledge"] += 1
            a_points -= 1
        else:
            print("Input a number between 1 and 4")
    character.reset_default_stats()
    return character

class battle: #This is the class we use to create and moniter battles
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def turn_cycle(self, player, enemy): #This cycles through player and enemy turns until enough wounds have been inflicted to either one
        while player.Wounds < player.WoundThreshold and enemy.Wounds < enemy.WoundThreshold:
            while player.ActionPoints > 0 and player.Wounds < player.WoundThreshold and enemy.Wounds < enemy.WoundThreshold:
                player.display_combat_stats()
                enemy.display_combat_stats()
                player.display_actions()
                player.player_action(enemy)
            player.recover_AP()
            while enemy.ActionPoints > 0 and player.Wounds < player.WoundThreshold and enemy.Wounds < enemy.WoundThreshold:
                player.display_combat_stats()
                enemy.display_combat_stats()
                enemy.enemy_action(player)
            enemy.recover_AP()

        if enemy.Wounds >= enemy.WoundThreshold:
            print(player.name, " has defeated ", enemy.name, "!")
            player.reset_default_stats
            enemy.reset_default_stats
        if player.Wounds >= player.WoundThreshold:
            print("Alas, ", player.name, " has fallen before ", enemy.name, "...")
            player.reset_default_stats
            enemy.reset_default_stats
            import sys #This ends the game if the player uses. Was experimenting with a "Continue" option, but its 2:30 AM
            sys.exit()

            

    

print("First, tell me your name...")
player_name = str(input())
hero = character(player_name) #Gets the hero's name and creates the initial character
character_creation(hero)
hero.reset_default_stats()#After we create the character, we must update their stats to remain in sync with their attributes

bandit = character("The Cursed Bandit") #The first enemy is created
bandit.tactics.append("ATTACK")#their tactics are added to the tactics list
bandit.tactics.append("ATTACK")
bandit.tactics.append("ATTACK")
bandit.tactics.append("UNHOLY RAGE")
bandit.tactics.append("DEFEND")
bandit.tactics.append("MEND FLESH")
bandit.attributes["Strength"] += 2
bandit.attributes["Agility"] += 0
bandit.attributes["Vitality"] += 1
bandit.attributes["Knowledge"] += 0
bandit.reset_default_stats() #Their attributes are edited and accounted for

bandit_fight = battle(hero, bandit) #We create a fight between the hero and the bandit
print("A bandit approaches. He is wielding a strange blade, the color of blood diamonds. Prepare to fight")
bandit_fight.turn_cycle(hero, bandit) #We go through the turn cycle to resolve the fight
level_up(hero) #The hero gains more attribute points
print("1: With the bandit dead, The Red Sword lays unclaimed. You could take it.")
print("2: Or you could search his journal to learn the magic he used to heal himself")
print("Which will you choose?")
choice1 = int(input()) #The hero chooses which ability they wish to learn from the enemy
if choice1 == 1:
    hero.possible_actions.append("UNHOLY RAGE")
if choice1 == 2:
    hero.possible_actions.append("MEND FLESH")
hero.display_combat_stats()

sorcerer = character("Robed Sorceress") #Rinse and repeat
sorcerer.tactics.append("BATTLE ZEN")
sorcerer.tactics.append("DEFEND")
sorcerer.tactics.append("DEFEND")
sorcerer.tactics.append("ATTACK")
sorcerer.tactics.append("DEFEND")
sorcerer.tactics.append("ATTACK")
sorcerer.tactics.append("DEFEND")
sorcerer.tactics.append("ATTACK")
sorcerer.tactics.append("HEX")
sorcerer.tactics.append("ATTACK")
sorcerer.tactics.append("DEFEND")
sorcerer.attributes["Strength"] += 0
sorcerer.attributes["Agility"] += 2
sorcerer.attributes["Vitality"] += 1
sorcerer.attributes["Knowledge"] += 5
sorcerer.reset_default_stats()

sorceress_fight = battle(hero, sorcerer)
print("A mysterious figure in robes approaches. She twirls a quarterstaff deftly and is poised to attack")
sorceress_fight.turn_cycle(hero, sorcerer)
level_up(hero)
print("1: The sorceresses grimoire contains many spells, including the dark magic hex she cast")
print("2: There is also an entry describing the art of combat meditation")
print("Which will you choose?")
choice2 = int(input())
if choice2 == 1:
    hero.possible_actions.append("HEX")
    print(hero.name, "has chosen the Hex \n")
if choice2 == 2:
    hero.possible_actions.append("BATTLE ZEN")
    print(hero.name, "has chosen Battle Zen \n")
hero.display_combat_stats()


yorick = character("Blademaster Yorick")
yorick.tactics.append("DEFEND")
yorick.tactics.append("WAIT")
yorick.tactics.append("ATTACK")
yorick.tactics.append("ATTACK")
yorick.tactics.append("ATTACK")
yorick.tactics.append("DEFEND")
yorick.tactics.append("DEFEND")
yorick.tactics.append("ATTACK")
yorick.tactics.append("ATTACK")
yorick.tactics.append("ATTACK")
yorick.tactics.append("DEFEND")
yorick.tactics.append("ATTACK")
yorick.tactics.append("ATTACK")
yorick.tactics.append("STOP TIME")
yorick.tactics.append("ATTACK")
yorick.tactics.append("ATTACK")
yorick.tactics.append("ATTACK")
yorick.tactics.append("ATTACK")
yorick.tactics.append("ATTACK")
yorick.tactics.append("ATTACK")
yorick.tactics.append("SUMMON DEATH")
yorick.attributes["Strength"] += 2
yorick.attributes["Agility"] += 3
yorick.attributes["Vitality"] += 1
yorick.attributes["Knowledge"] += 10
yorick.reset_default_stats()

yorick_fight = battle(hero, yorick)
print("A mysterious figure in robes approaches. She twirls a quarterstaff deftly and is poised to attack")
yorick_fight.turn_cycle(hero, yorick)
level_up(hero)
level_up(hero)
print("1: Adorned on Yorick's right hand blade is the secret to stopping time")
print("2: On his off hand blade is the name of death itself")
print("Which will you choose?")
choice3 = int(input())
if choice3 == 1:
    hero.possible_actions.append("STOP TIME")
if choice3 == 2:
    hero.possible_actions.append("SUMMON DEATH")
hero.display_combat_stats()


titan = character("The Mad Titan")
titan.tactics.append("ATTACK")
titan.tactics.append("ATTACK")
titan.tactics.append("ATTACK")
titan.tactics.append("HEX")
titan.tactics.append("HEX")
titan.tactics.append("DEFEND")
titan.attributes["Strength"] += 7
titan.attributes["Agility"] += 7
titan.attributes["Vitality"] += 10
titan.attributes["Knowledge"] += 3
titan.reset_default_stats()

titan_fight = battle(hero, titan)
print("The Mad Titan has awakened, and hell follows him")
titan_fight.turn_cycle(hero, titan)

print("With the titan slain, you have completed The Gauntlet of Power")

