# -*- coding: utf-8 -*-
from .system import Engine
import rpgbattle.system


class Action(Engine):
    @property
    def target_types(self):
        return self.__target_types

    @target_types.setter
    def target_types(self, target_types):
        self.__target_types = target_types

    def execute(self, source, targets):
        "Performs the action and applies all effects. Returns an array of strings that describe what has happened"
        return [0]

    def __str__(self):
        return self.__class__.__name__



class Attack(Action):

    target_types = ["single"]

    def __init__(self):
        super(Attack, self).__init__()

    def execute(self, source, targets):
        target = targets[0]  # Attack can only target one character
        dmg = self.system.calculateDamage(
            source.stat["patt"], target.stat["pdef"])
        dmg = self.system.applyDamage(dmg, "hp", target)
        return ["{0} deals {1} damage to {2}".format(source, dmg, target)]


class Dark(Action):

    target_types = ["party"]

    def __init__(self):
        super(Dark, self).__init__()

    def execute(self, source, targets):
        dmglist = []
        for target in targets:
            dmg = self.system.calculateDamage(
                source.stat["patt"], target.stat["pdef"])
            dmg = self.system.applyDamage(dmg, "hp", target)
            dmglist.append(
                "{0} deals {1} damage to {2}".format(source, dmg, target))
        return dmglist


class Heal(Action):
    target_types = ["single"]

    def __init__(self):
        super(Heal, self).__init__()

    def execute(self, source, targets):
        target = targets[0]
        dmg = self.system.applyHealing(12, 'hp', target)
        return ["{0} heals {1}hp to {2}".format(source, dmg, target)]
