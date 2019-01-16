# -*- coding: utf-8 -*-
from random import uniform as rand
from . import character as char
from time import sleep
import math


class System:
    randvar = 5

    def __init__(self, randvar):
        "Sets the random variation as a + or - percentile (0-100)"
        self.randvar = randvar / 100

    def randVar(self, damage):
        "Returns a floored value with random variation factored in"
        var = self.randvar
        return math.floor(rand(damage * (1 - var), damage * (1 + var)))

    def calculateDamage(self, att, deff):
        "This is the default damage"
        return self.randVar(att * 2 * (511 - deff) / 511)

    def applyDamage(self, damage, stat, target):
        new_stat = min((9999, max((-1, target.getStat(stat) - damage))))
        target.stat[stat] = new_stat
        return damage

    def applyHealing(self, healing, stat, target):
        dmg = self.randVar(healing)
        new_stat = max((target.getInitialStat(
            stat), target.getStat(stat) + dmg))
        target.stat[stat] = new_stat
        return dmg


class Engine:
    system = System(randvar=5)

    def inputList(self, choices, prompt, returnValues=None):
        "Prints a list of choices on the screen with formatting"
        choice = None
        while choice is None:
            for i in range(len(choices)):
                print(("{} - {}".format(i + 1, choices[i])))
            try:
                action = int((input(prompt)))
                if action < 1:
                    continue
                if returnValues == None:
                    choice = choices[action - 1]
                else:
                    choice = returnValues[action - 1]
            except ValueError:
                continue
            except IndexError:
                continue
        return choice


class Party(Engine):
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def __init__(self, members, name):
        "Members is a list or tuple of Character class objects"
        self.members = members
        self.name = name
        super(Party, self).__init__()

    def __str__(self):
        return self.name


class Battle(Engine):

    def __init__(self, parties):
        "Parties is a list or tuple of Party class objects"
        super(Battle, self).__init__()
        self.parties = parties
        self.members = []
        for party in self.parties:
            self.members.extend(party.members)
        # Sort the members in order of initiative
        self.members = sorted(
            self.members, key=lambda member: member.stat['init'], reverse=True)

    def printCurrent(self, char):
        print('{} HP: {} / {}'.format(char.name,
                                      char.stat["hp"], char.initial_stat["hp"]))

    def notDeadMembers(self):
        "Gets all not dead members"
        return list(filter(lambda item: item.isDead() == False, self.members))

    def mainLoop(self):
        "Runs a battle till it ends"
        turns_played = 0
        while self.isBattleOver() is False:
            print(("\nTurn {}\n--------------------".format(turns_played + 1)))
            for i in range(len(self.members)):
                attacker = self.members[i]
                if (attacker.isDead()):
                    continue  # Go to the next character in the battle
                self.printCurrent(self.members[i])
                action = attacker.chooseAction()
                targets = attacker.chooseTarget(self, action)
                dmg = action.execute(attacker, targets)
                print(dmg)
                print()
                sleep(1.5)
                if self.isBattleOver():
                    # Exit the loop; it's over.
                    break
            turns_played += 1
        return turns_played

    def allDead(self, instance):
        for member in self.members:
            if isinstance(member, instance) and member.isDead() is False:
                return False
        return True

    def isBattleOver(self):
        return self.allDead(char.Ally) or self.allDead(char.Enemy)

    def isWin(self):
        if (self.isBattleOver() is False):
            return None
        else:
            return self.allDead(char.Enemy)

    def isLoss(self):
        return not(self.isWin())


class Buff(Engine):

    def __init__(self, duration):
        super(Buff, self).__init__()
        self.duration = duration
