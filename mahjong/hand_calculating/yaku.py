# -*- coding: utf-8 -*-


class Yaku(object):
    yaku_id = None
    tenhou_id = None
    name = None
    han_open = None
    han_closed = None
    is_yakuman = None
    english = None
    japanese = None

    def __init__(self, yaku_id=None):
        self.tenhou_id = None
        self.yaku_id = yaku_id

        self.set_attributes()

    def __str__(self):
        return self.name

    def __repr__(self):
        # for calls in array
        return self.__str__()

    def is_condition_met(self, hand, *args):
        """
        Is this yaku exists in the hand?
        :param: hand
        :param: args: some yaku requires additional attributes
        :return: boolean
        """
        raise NotImplementedError

    def set_attributes(self):
        """
        Set id, name, han related to the yaku
        """
        raise NotImplementedError
