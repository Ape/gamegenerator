from enum import Enum

Color = Enum("Color", "red green blue yellow")

def wire_colors():
    return list(Color)

def victory(wires):
    # You win the game when there are no red wires.
    return all((x != Color.red for x in wires))

def actions():
    return [
        # Cut a red wire if the previous wire is green or if there is no
        # previous wire, and if the next wire is blue or if there is no next
        # wire.
        lambda wires, cut: wires[cut] == Color.red \
                           and _prev(wires, cut) in [None, Color.green] \
                           and _first(wires, cut+1) in [None, Color.blue],

        # Cut a red wire with exactly two wires before it if the first wire
        # after is also red and the second wire after is not red.
        lambda wires, cut: wires[cut] == Color.red \
                           and _num(wires[:cut]) == 2 \
                           and _first(wires, cut+1) == Color.red \
                           and _first(wires, cut+2) != Color.red,

        # Cut a green wire if the next wire is yellow and there is an odd
        # number of green wires.
        lambda wires, cut: wires[cut] == Color.green \
                           and _first(wires, cut+1) == Color.yellow \
                           and _num_color(wires, Color.green) % 2 == 1,

        # Cut a green wire if there is exactly one yellow wire and exactly one
        # green wire.
        lambda wires, cut: wires[cut] == Color.green \
                           and _num_color(wires, Color.green) == 1 \
                           and _num_color(wires, Color.yellow) == 1,

        # Cut a green wire if the last wire is blue and there is an even number
        # of green wires.
        lambda wires, cut: wires[cut] == Color.green \
                           and _prev(wires, len(wires)) == Color.blue \
                           and _num_color(wires, Color.green) % 2 == 0,

        # Cut a blue wire if there are exactly four wires.
        lambda wires, cut: wires[cut] == Color.blue \
                           and _num(wires) == 4,

        # Cut a blue wire if there are as many red wires as there are blue and
        # yellow wires combined.
        lambda wires, cut: wires[cut] == Color.blue \
                           and (_num_color(wires, Color.blue)
                                + _num_color(wires, Color.yellow)
                                == _num_color(wires, Color.red)),

        # Cut a yellow wire if the first wire is green and there is an even
        # number of yellow wires.
        lambda wires, cut: wires[cut] == Color.yellow \
                           and _first(wires, 0) == Color.green \
                           and _num_color(wires, Color.yellow) % 2 == 0,

        # Cut a yellow wire if the first wire is blue and there is an odd
        # number of yellow wires.
        lambda wires, cut: wires[cut] == Color.yellow \
                           and _first(wires, 0) == Color.blue \
                           and _num_color(wires, Color.yellow) % 2 == 1,

        # Cut a yellow wire if the next wire is red and the previous wire is
        # not yellow.
        lambda wires, cut: wires[cut] == Color.yellow \
                           and _prev(wires, cut) != Color.yellow \
                           and _first(wires, cut+1) == Color.red,

        # Cut any wire that is not red or green if it is between two green
        # wires with no other colors in between.
        lambda wires, cut: not wires[cut] in [Color.red, Color.green] \
                           and _prev(wires, cut) == Color.green \
                           and _first(wires, cut+1) == Color.green,
    ]

def _num(wires):
    return sum((1 for x in wires if x != None))

def _num_color(wires, color):
    return sum((1 for x in wires if x == color))

def _first(wires, index):
    try:
        return next((x for x in wires[index:] if x != None))
    except StopIteration:
        return None

def _prev(wires, index):
    try:
        return next((x for x in reversed(wires[:index]) if x != None))
    except StopIteration:
        return None
