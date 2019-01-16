# -*- coding: utf-8 -*-


class NegativeStatException(Exception):

    def __init__(self, arg):
        super(NegativeStatException, self).__init__(arg)
