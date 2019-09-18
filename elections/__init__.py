import os
import pickle

import us

from elections.models.elections import GeneralElection, PrimaryElection
from elections.models.seats import HouseSeat, SenateSeat
from elections.models.parties import Party
from elections.utils.getters import get_party
from elections.utils.builts import (
    ChamberFilterableList,
    ElectionTypeFilterableList,
)

PWD = os.path.abspath(os.path.dirname(__file__))


class InvalidYear(Exception):
    pass


def load_years():
    from pkg_resources import resource_stream

    years = []
    with resource_stream(__name__, "data/years.pkl") as pklfile:
        for d in pickle.load(pklfile):
            years.append(d)
    return years


class ElectionYear(object):
    def __init__(self, year):
        year = str(year)
        if year not in load_years():
            raise InvalidYear(
                "No data available for the {} election cycle".format(year)
            )
        self.year = year
        self.incumbent_parties = self.load_parties()
        self.seats = self.load_seats()
        self.elections = self.load_elections()

    def load_parties(self):
        from pkg_resources import resource_stream

        parties = []
        with resource_stream(__name__, "data/parties.pkl") as pklfile:
            for d in pickle.load(pklfile):
                parties.append(Party(**d))
        return parties

    def assign_parties_to_seats(self, seats):
        for seat in seats:
            holding_party = get_party(
                getattr(seat, "incumbent_party", None), self.incumbent_parties
            )
            if holding_party:
                holding_party.add_held_seat(seat)
                seat.incumbent_party = holding_party
        # filter out parties that don't hold any seats
        self.incumbent_parties = list(
            filter(lambda d: d.holds_seats, self.incumbent_parties)
        )
        return seats

    def load_seats(self):
        from pkg_resources import resource_stream

        seats = ChamberFilterableList()
        with resource_stream(
            __name__, "data/{}/seats.pkl".format(self.year)
        ) as pklfile:
            for d in pickle.load(pklfile):
                if d["seat_type"] == "house":
                    seats.append(HouseSeat(**d))
                elif d["seat_type"] == "senate":
                    seats.append(SenateSeat(**d))
        return self.assign_parties_to_seats(seats)

    def load_elections(self):
        from pkg_resources import resource_stream

        elections = ElectionTypeFilterableList()
        with resource_stream(
            __name__, "data/{}/elections.pkl".format(self.year)
        ) as pklfile:
            for d in pickle.load(pklfile, encoding="latin1"):
                if d["election_type"] == "general":
                    elections.append(GeneralElection(**d))
                elif d["election_type"] == "primary":
                    elections.append(PrimaryElection(**d))
        return elections

    def seats_for_state(self, state):
        state = us.states.lookup(state)
        return ChamberFilterableList(
            [seat for seat in self.seats if seat.state == state]
        )

    def elections_for_state(self, state):
        state = us.states.lookup(state)
        return ElectionTypeFilterableList(
            [
                election
                for election in self.elections
                if election.state == state
            ]
        )
