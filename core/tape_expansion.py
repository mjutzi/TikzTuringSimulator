import collections


def left_of_expandable(index, list, placeholder=None):
    new_index = index - 1
    while new_index < 0:
        list.insert(0, placeholder)
        new_index += 1
    return new_index


def left_of_unexpandable(index, list, placeholder=None):
    new_index = index - 1
    if new_index < 0:
        raise ValueError('Index out of left range.')
    return new_index


def right_of_expandable(index, list, placeholder=None):
    new_index = index + 1
    while new_index >= len(list):
        list.append(placeholder)
        new_index -= 1
    return new_index


def right_of_unexpandable(index, list, placeholder=None):
    new_index = index + 1
    if new_index >= len(list):
        raise ValueError('Index out of right range.')
    return new_index

ExpansionStrategy = collections.namedtuple('ExpansionStrategy', 'move_left_op move_right_op')

EXPAND_ALL = ExpansionStrategy(move_left_op=left_of_expandable, move_right_op=right_of_expandable)

EXPAND_NONE = ExpansionStrategy(move_left_op=left_of_unexpandable, move_right_op=right_of_unexpandable)

EXPAND_LEFT_ONLY = ExpansionStrategy(move_left_op=left_of_expandable, move_right_op=right_of_unexpandable)

EXPAND_RIGHT_ONLY = ExpansionStrategy(move_left_op=left_of_unexpandable, move_right_op=right_of_expandable)
