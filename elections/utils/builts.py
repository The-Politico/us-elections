from elections.models.elections import GeneralElection, PrimaryElection
from elections.models.seats import HouseSeat, SenateSeat


class ChamberFilterableList(list):
    @property
    def senate(self):
        return [
            seat for seat in self.__iter__() if isinstance(seat, SenateSeat)
        ]

    @property
    def house(self):
        return [
            seat for seat in self.__iter__() if isinstance(seat, HouseSeat)
        ]


class ElectionTypeFilterableList(list):
    @property
    def general(self):
        return [
            election
            for election in self.__iter__()
            if isinstance(election, GeneralElection)
        ]

    @property
    def primary(self):
        return [
            election
            for election in self.__iter__()
            if isinstance(election, PrimaryElection)
        ]
