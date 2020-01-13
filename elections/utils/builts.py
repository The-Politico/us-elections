# Imports from us-elections.
from elections.models.elections import DemocraticPrimaryElection
from elections.models.elections.primary_runoff import (
    DemocraticPrimaryRunoffElection,
)
from elections.models.elections import GeneralElection
from elections.models.elections import PrimaryElection
from elections.models.elections.primary_runoff import PrimaryRunoffElection
from elections.models.elections import RepublicanPrimaryElection
from elections.models.elections.primary_runoff import (
    RepublicanPrimaryRunoffElection,
)
from elections.models.electoral_votes import DistrictElectoralZone
from elections.models.electoral_votes import StateElectoralZone
from elections.models.seats import HeadOfGovernmentSeat
from elections.models.seats import HouseSeat
from elections.models.seats import SenateSeat


PARTISAN_ELECTION_TYPES = {
    "democratic": {
        "primary": DemocraticPrimaryElection,
        "primary_runoff": DemocraticPrimaryRunoffElection,
    },
    "republican": {
        "primary": RepublicanPrimaryElection,
        "primary_runoff": RepublicanPrimaryRunoffElection,
    },
}

TO_WORD_ORDINALS = ["first", "second", "third"]


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


class ExecutiveSeatFilterableList(list):
    @property
    def chief(self):
        chiefs = [
            seat
            for seat in self.__iter__()
            if isinstance(seat, HeadOfGovernmentSeat)
        ]
        if len(chiefs) > 1:
            raise ValueError(
                "State and federal executive branches have only one "
                "Head of Government."
            )
        return chiefs[0] if len(chiefs) == 1 else None

    @property
    def lower_seats(self):
        return [
            seat
            for seat in self.__iter__()
            if not isinstance(seat, HeadOfGovernmentSeat)
        ]


class StateFilterableList(list):
    def add_state(self, state_name, state_government_obj):
        setattr(self, state_name, state_government_obj)
        self.append(state_government_obj)


class PartisanElectionFilterableList(list):
    @property
    def democratic(self):
        return [
            election
            for election in self.__iter__()
            if any(
                [
                    isinstance(election, Klass)
                    for election_type, Klass in PARTISAN_ELECTION_TYPES[
                        "democratic"
                    ].items()
                    if Klass
                ]
            )
        ]

    @property
    def republican(self):
        return [
            election
            for election in self.__iter__()
            if any(
                [
                    isinstance(election, Klass)
                    for election_type, Klass in PARTISAN_ELECTION_TYPES[
                        "republican"
                    ].items()
                    if Klass
                ]
            )
        ]


class ElectionTypeFilterableList(list):
    @property
    def general_elections(self):
        return [
            election
            for election in self.__iter__()
            if isinstance(election, GeneralElection)
        ]

    @property
    def primaries(self):
        return PartisanElectionFilterableList(
            [
                election
                for election in self.__iter__()
                if isinstance(election, PrimaryElection)
                and not isinstance(election, PrimaryRunoffElection)
            ]
        )

    @property
    def primary_runoffs(self):
        return PartisanElectionFilterableList(
            [
                election
                for election in self.__iter__()
                if isinstance(election, PrimaryRunoffElection)
            ]
        )

    @property
    def presidential_primaries(self):
        return PartisanElectionFilterableList(
            [
                election
                for election in self.__iter__()
                if election.election_date.year % 4 == 0
                and isinstance(election, PrimaryElection)
                and not isinstance(election, PrimaryRunoffElection)
                and getattr(election, "election_level", "")
                in ["president", "all"]
            ]
        )

    @property
    def downticket_primaries(self):
        return PartisanElectionFilterableList(
            [
                election
                for election in self.__iter__()
                if isinstance(election, PrimaryElection)
                and not isinstance(election, PrimaryRunoffElection)
                and getattr(election, "election_level", "all")
                in ["all", "downticket"]
            ]
        )


class ElectoralVoteFilterableList(list):
    def add_zone(self, electoral_zone):
        state_slug = electoral_zone.state.name.replace(" ", "_").lower()

        if isinstance(electoral_zone, StateElectoralZone):
            setattr(self, state_slug, electoral_zone)
        else:
            setattr(
                self,
                "{}_{}_district".format(
                    state_slug,
                    TO_WORD_ORDINALS[int(electoral_zone.district) - 1],
                ),
                electoral_zone,
            )
        self.append(electoral_zone)

    @property
    def statewide(self):
        return [
            electoral_zone
            for electoral_zone in self.__iter__()
            if isinstance(electoral_zone, StateElectoralZone)
        ]

    @property
    def by_district(self):
        return [
            electoral_zone
            for electoral_zone in self.__iter__()
            if isinstance(electoral_zone, DistrictElectoralZone)
        ]
