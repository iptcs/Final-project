# Final-project
Final project for intro to python class
This is a basic turn based boss rush with light RPG elements, in text form

There are no tricks to running the file properly; any Python shell should do fine. Just start it up

Here is a rundown of how to play effectively
In this game, 'attributes' are values which are used to determine other values called 'stats'. When you create and name your character you will get the opportunity to increase them.

Attributes do not TECHNICALLY directly affect your character's abiliites for the most part(how much damage you do, etc). Instead, they are used to calculate stats, which do directly affect these things. The trick is that each stat is derrived from at least 2 different attributes, so to maximize its power you need to upgrade both. This limits the amount of control you have over exactly what you can do, and forces you to compromise. If you want to deal as much damage as possible in melee, you can't also have lots of mana.

Here is brief rundown of what each attribute does

Agility - Contributes to attack damage. Directly determines how quickly you regain Defense Points, which are sort of like Hit Points, except that you don't die when they are gone; instead you start taking wounds, the things that actually kill you. When you use the Defend command to regain DP (Defense Points), Agility controls how many you get. Agility also governs how many Action Points you have at the start of a fight, which are what you expend to take action.

Strength - Contirbutes to attack damage and wound threshold (how many hits you take before you die). It also affects how many wounds you INFLICT, which is seperate from raw damage dealt.

Vitality - Vitality contributes to your wound threshold along with Strength, and your mana along with Knowledge. It also plays the important role of determining how quickly you regain spent AP (Action Points).

Knowledge - Contributes to mana, and also determines how much DP you start a fight with, representing your experience with combat and ability to think ahead. It's true use doesn't really become apperant until you get your first spell, and need mana to cast it. Mana, unlike other resources, does not regenerate during combat.

Stats:
Attack = Strength + Agility
Starting and Max DP = Knowledge +9
Wound Threshold = Vitality + Strength
Starting and Max AP = Agility
Mana and Max Mana = Vitality + Knowledge +3

Basic actions:
Attack - deals damage 1-3 damage + your Strength and Agility to targets DP. Also deals your Strength in wounds to anyone without DP, either becaue they never had any or because you stripped it with your attack

Defend - Boost your DP by a number equal to your Agility. Can't go past the maximum.

Wait - Do nothing. Your opponent will get to act, but you will regain extra AP this turn.

Descriprion of spells:
Unholy Rage: 2 mana - Essentially an attack that deals extra wounds and damage equal to your maximum mana. The more knowledge and vitality you have, the stronger it is

Mend Flesh: 2 mana - Removes a single wound from the user

Battle Zen: 4 mana - Gives a +5 boost to maximum DP which lasts all fight, and raises current DP by the resultant maximum. Also grants a +1 to DP recovery for the duration of the battle.

Hex: 4 mana - A magical blast that deals damage equal to 3 times the casters Knowledge. Also inflicts wounds equal to Knowledge to anyone whose DP is at or reduced to 0.

Summon Death: 5 mana - Literally summon the grim reaper. It has a 2/3 chance of instantly killing the target, and a 1/3 chance of reducing the caster's wound threshold by 1 for the rest of the fight. This turned out really overpowered, might nerf it later.

Stop Time: 10 mana - Gives you AP equal to twice your max, effectively allowing you to take a fuck ton of turns in a row. Similarly overpowered, but you at least need 10 mana to cast it, which you are not garaunteed to ever have.
