# -*- coding: utf-8 -*-
from .system import Engine, BackAMenu
from .action import Attack, Dark, Heal
from random import choice, randrange
import math


class Character(Engine):
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def __init__(self, hp, patt, pdef, init, actions=[Attack()]):
        self.initial_stat = {"hp": hp, "patt": patt,
                             "pdef": pdef, "init": init}
        self.stat = self.initial_stat.copy()
        self.name = self.__class__.__name__
        self.actions = actions

    @property
    def actions(self):
        return self.__actions

    @actions.setter
    def actions(self, actions):
        self.__actions = actions

    @property
    def stat(self):
        return self.__stat

    @stat.setter
    def stat(self, stats):
        # Need to implement some error checking
        self.__stat = stats

    @property
    def initial_stat(self):
        return self.__initial_stat

    @initial_stat.setter
    def initial_stat(self, stats):
        # Need to implement some error checking
        self.__initial_stat = stats

    def getStat(self, stat):
        return self.stat[stat]

    def getInitialStat(self, stat):
        return self.initial_stat[stat]

    def isDead(self):
        return self.stat["hp"] < 1

    def chooseAction(self):
        raise NotImplementedError

    def chooseTarget(self, battle, action):
        raise NotImplementedError

    def __str__(self):
        st = self.name
        if (self.isDead()):
            st += " (Dead)"
        return st


class Ally(Character):
    def __init__(self, name, hp, patt, pdef, init, actions=[Attack(), Dark()]):
        super(Ally, self).__init__(hp, patt, pdef, init, actions=actions)
        self.name = name

    def chooseAction(self):
        return self.inputList(self.actions, "Please choose an action for {}: ".format(self))

    def chooseTarget(self, battle, action):
        target_type = self.chooseTargetType(action)
        if (isinstance(target_type, BackAMenu)):
            return target_type
        # Now pick the target based on the type
        target = None
        while target is None:
            if (target_type == 'single'):
                target_list = list(map(lambda value: "{} {}/{} HP".format(
                    value, value.stat['hp'], value.initial_stat['hp']), battle.notDeadMembers()))
                target = self.inputList(
                    target_list, "Please choose a target: ", returnValues=battle.notDeadMembers(), goBack=True)
                if not isinstance(target, BackAMenu):
                    target = [target]
            elif (target_type == 'party'):
                target = self.inputList(
                    battle.parties, "Please choose a target: ", goBack=True)
                if not isinstance(target, BackAMenu):
                    target = target.members
            elif (target_type == 'all'):
                target = battle.members
        return target

    def chooseTargetType(self, action):
        target_types = action.target_types
        target_type = None
        if (len(target_types) == 1):
            target_type = target_types[0]
        else:
            while target_type is None:
                target_type = self.inputList(
                    target_types, "Please choose a target type: ", goBack=True)
        return target_type


class Enemy(Character):
    def __init__(self, hp, patt, pdef, init):
        super(Enemy, self).__init__(hp, patt, pdef, init)

    def chooseAction(self):
        return self.actions[0]

    def chooseTarget(self, battle, action, partyName="Allies"):
        # Select the allies
        for party in battle.parties:
            if party.name == partyName:
                target_party = party
                break
        # Select random party member
        target = choice(self.notDeadMembers(target_party.members))
        return [target]


class Boss(Enemy):
    last_attack = None

    def __init__(self, hp, patt, pdef, init):
        super(Boss, self).__init__(hp, patt, pdef, init)
        self.actions = [Attack(), Dark(), Heal()]

    def chooseAction(self):
        if (self.getStat('hp') < .15 * self.getInitialStat('hp')):
            # Heal
            return self.actions[2]
        dice_roll = randrange(1, stop=6)
        if (dice_roll >= 1 and dice_roll < 4):
            # Attack
            return self.actions[0]
        else:
            # dark
            return self.actions[1]

    def chooseTarget(self, battle, action):
        if (isinstance(action, Attack)):
            return super().chooseTarget(battle, action)
        elif isinstance(action, Dark):
            return self.notDeadMembers(battle.parties[0].members)
        else:
            # Healz
            return [self]
