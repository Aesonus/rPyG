# -*- coding: utf-8 -*-
from rpgbattle.character import Ally, Enemy
from rpgbattle.action import Attack, Heal
import rpgbattle.system as system

ally = Ally("Healer", 100, 2, 2, 4, actions=[Attack(), Heal()])
ally2 = Ally("Attacker", 120, 7, 3, 2)

allyParty = system.Party((ally, ally2), "Allies")
enemyParty = system.Party([Enemy(15, 5, 4, 3), Enemy(15, 5, 4, 5)], "Enemies")
battle = system.Battle([allyParty, enemyParty])

turns = battle.mainLoop()

# See who won
if battle.isLoss():
    print("Shit...")
elif battle.isWin():
    print("You win! WOO!")

print(("\nThe fight was over in {} turns".format(turns)))
