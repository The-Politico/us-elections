# Imports from us-elections.
from elections.utils.builts import ChamberFilterableList


class Party(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v
        self.held_seats = ChamberFilterableList()

    def add_held_seat(self, seat):
        self.held_seats.append(seat)

    @property
    def holds_seats(self):
        return len(self.held_seats) > 0

    def __repr__(self):
        return "<Party: {}>".format(self.__str__())

    def __str__(self):
        return self.name
