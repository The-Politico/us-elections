# Imports from python.
import pickle


# Imports from other dependencies.
import us


# Imports from us-elections.
from elections.exceptions import InvalidYear
from elections.models.elections import GeneralElection
from elections.models.elections import DemocraticPrimaryElection
from elections.models.elections import DemocraticPrimaryRunoffElection
from elections.models.elections import PrimaryElection
from elections.models.elections import PrimaryRunoffElection
from elections.models.elections import RepublicanPrimaryElection
from elections.models.elections import RepublicanPrimaryRunoffElection
from elections.models.electoral_votes import DistrictElectoralZone
from elections.models.electoral_votes import StateElectoralZone
from elections.models.governments.constants import LEGISLATIVE
from elections.models.governments.constants import EXECUTIVE
from elections.models.governments.constants import JUDICIAL
from elections.models.governments import FederalGovernment
from elections.models.governments import StateGovernment
from elections.models.seats import ExecutiveSeat
from elections.models.seats import HeadOfGovernmentSeat
from elections.models.seats import HouseSeat
from elections.models.seats import SenateSeat
from elections.models.parties import Party
from elections.utils.alternative_areas import alternative_areas
from elections.utils.getters import get_party
from elections.utils.builts import ChamberFilterableList
from elections.utils.builts import ElectionTypeFilterableList
from elections.utils.builts import ElectoralVoteFilterableList
from elections.utils.builts import ExecutiveSeatFilterableList
from elections.utils.builts import StateFilterableList
from elections.utils.constants import ELECTION_YEAR_TYPES
from elections.utils.constants import FIRST_PRESIDENTIAL_ELECTION
from elections.utils.constants import MIDTERM_YEAR_TYPE
from elections.utils.constants import PRESIDENTIAL_ELECTION_INTERVAL
from elections.utils.constants import PRESIDENTIAL_YEAR_TYPE
from elections.utils.data_loaders import load_pickled_data


def load_years():
    years = []
    with load_pickled_data("data/years.pkl") as pklfile:
        for d in pickle.load(pklfile):
            years.append(d)
    return years


CHAMBER_ORDER = ["senate", "house"]


class ElectionYear(object):
    def __init__(self, year, **kwargs):
        year = str(year)
        year_as_int = int(year)
        if year not in load_years():
            raise InvalidYear(
                "No data available for the {} election cycle".format(year)
            )
        self.year = year

        self.include_states = True

        for k, v in kwargs.items():
            if k == "include_states":
                self.include_states = bool(v)
            else:
                self.__dict__[k] = v

        self.incumbent_parties = self.load_parties()

        self.election_year_type = ELECTION_YEAR_TYPES[
            (year_as_int - FIRST_PRESIDENTIAL_ELECTION)
            % PRESIDENTIAL_ELECTION_INTERVAL
        ]

        patched_federal_jurisdiction = us.unitedstatesofamerica
        patched_federal_jurisdiction.ap_abbr = "U.S."

        federal_government_params = {
            "jurisdiction": patched_federal_jurisdiction,
            LEGISLATIVE: (
                self.load_federal_legislative_seats()
                if self.election_year_type
                in [PRESIDENTIAL_YEAR_TYPE, MIDTERM_YEAR_TYPE]
                else []
            ),
            EXECUTIVE: (
                self.load_federal_executive_seats()
                if self.election_year_type == PRESIDENTIAL_YEAR_TYPE
                else []
            ),
            JUDICIAL: [],  # No federal judiciary members are elected.
        }

        if self.election_year_type == PRESIDENTIAL_YEAR_TYPE:
            federal_government_params[
                "electoral_votes"
            ] = self.load_electoral_votes()

        self.federal = FederalGovernment(**federal_government_params)

        if self.include_states:
            self.states = self.load_states()

        self.elections = self.load_elections()

    def load_parties(self):
        parties = []
        with load_pickled_data("data/parties.pkl") as pklfile:
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

    def load_federal_legislative_seats(self):
        seats = []
        with load_pickled_data(
            "data/{}/federal-legislative-seats.pkl".format(self.year)
        ) as pklfile:
            for d in pickle.load(pklfile):
                if d["seat_type"] == "house":
                    seats.append(HouseSeat(**d))
                elif d["seat_type"] == "senate":
                    seats.append(SenateSeat(**d))

        sorted_seats = sorted(
            seats,
            key=lambda x: int(getattr(x, "district", "0"))
            if hasattr(x, "district") and x.district is not None
            else 0,
        )
        sorted_seats = sorted(
            sorted_seats, key=lambda x: len(getattr(x, "senate_class", "IIII"))
        )
        sorted_seats = sorted(sorted_seats, key=lambda x: x.state.name)
        sorted_seats = sorted(
            sorted_seats, key=lambda x: CHAMBER_ORDER.index(x.seat_type)
        )

        return self.assign_parties_to_seats(
            ChamberFilterableList(sorted_seats)
        )

    def load_federal_executive_seats(self):
        seats = ExecutiveSeatFilterableList()
        with load_pickled_data(
            "data/{}/federal-executive-seats.pkl".format(self.year)
        ) as pklfile:
            for d in pickle.load(pklfile):
                if d["office"] == "president":
                    seats.append(HeadOfGovernmentSeat(**d))
                else:
                    seats.append(ExecutiveSeat(**d))

        seats = self.assign_parties_to_seats(seats)

        return seats

    def load_electoral_votes(self):
        if self.election_year_type != PRESIDENTIAL_YEAR_TYPE:
            raise ValueError(
                "Only presidential election years have electoral votes."
            )

        vote_zones = ElectoralVoteFilterableList()
        with load_pickled_data(
            "data/{}/electoral-votes.pkl".format(self.year)
        ) as pklfile:
            for d in pickle.load(pklfile):
                if d["type"] == "statewide":
                    vote_zones.add_zone(StateElectoralZone(**d))
                else:
                    vote_zones.add_zone(DistrictElectoralZone(**d))

        # vote_zones = self.assign_states_to_vote_zones(vote_zones)

        return vote_zones

    def load_states(self):
        state_list = StateFilterableList()

        for state in us.STATES:
            if state.statehood_year:  # Taxation w/o representation! Nix D.C.
                state.slug = state.name.replace(" ", "_").lower()
                state_list.add_state(
                    state.slug,
                    StateGovernment(
                        **{
                            "jurisdiction": state,
                            LEGISLATIVE: (
                                self.load_state_legislative_seats(
                                    state.abbr.lower()
                                )
                            ),
                            EXECUTIVE: (
                                self.load_state_executive_seats(
                                    state.abbr.lower()
                                )
                            ),
                            JUDICIAL: [],
                        }
                    ),
                )

        return state_list

    def load_state_legislative_seats(self, state_abbr):
        seats = []
        with load_pickled_data(
            "data/{}/{}-legislative-seats.pkl".format(self.year, state_abbr)
        ) as pklfile:
            for d in pickle.load(pklfile):
                if d["seat_type"] == "house":
                    seats.append(HouseSeat(**d))
                elif d["seat_type"] == "senate":
                    seats.append(SenateSeat(**d))

        sorted_seats = sorted(
            seats, key=lambda x: CHAMBER_ORDER.index(x.seat_type)
        )

        return self.assign_parties_to_seats(
            ChamberFilterableList(sorted_seats)
        )

    def load_state_executive_seats(self, state_abbr):
        seats = ExecutiveSeatFilterableList()
        with load_pickled_data(
            "data/{}/{}-executive-seats.pkl".format(self.year, state_abbr)
        ) as pklfile:
            for d in pickle.load(pklfile):
                if d["office"] == "governor":
                    seats.append(HeadOfGovernmentSeat(**d))
                else:
                    seats.append(ExecutiveSeat(**d))

        return self.assign_parties_to_seats(seats)

    def load_elections(self):
        elections = []

        with load_pickled_data(
            "data/{}/elections.pkl".format(self.year)
        ) as pklfile:
            for d in pickle.load(pklfile, encoding="latin1"):
                if d["election_type"] == "general":
                    elections.append(GeneralElection(**d))
                elif d["election_type"] == "primary":
                    if d["election_party"] == "dem":
                        if d["election_date"] is not None:
                            elections.append(DemocraticPrimaryElection(**d))
                        if d["runoff_election_date"] is not None:
                            elections.append(
                                DemocraticPrimaryRunoffElection(**d)
                            )
                    elif d["election_party"] == "gop":
                        if d["election_date"] is not None:
                            elections.append(RepublicanPrimaryElection(**d))
                        if d["runoff_election_date"] is not None:
                            elections.append(
                                RepublicanPrimaryRunoffElection(**d)
                            )
                    else:
                        if d["election_date"] is not None:
                            elections.append(PrimaryElection(**d))
                        if d["runoff_election_date"] is not None:
                            elections.append(PrimaryRunoffElection(**d))

        sorted_elections = sorted(elections, key=lambda x: x.state.name)
        sorted_elections = sorted(
            sorted_elections, key=lambda x: x.election_date
        )

        return ElectionTypeFilterableList(sorted_elections)

    def elections_for_state(self, state_name_raw):
        state = us.states.lookup(state_name_raw)

        if not state:
            state = alternative_areas.get(state_name_raw, None)

        if not state:
            raise ValueError(f'No state found for query "{state_name_raw}".')

        return ElectionTypeFilterableList(
            [
                election
                for election in self.elections
                if election.state == state
            ]
        )

    def __repr__(self):
        return "<ElectionYear: {}>".format(self.__str__())

    def __str__(self):
        if self.election_year_type in [
            PRESIDENTIAL_YEAR_TYPE,
            MIDTERM_YEAR_TYPE,
        ]:
            return "{} ({} cycle)".format(
                self.year, self.election_year_type.capitalize()
            )
        return self.year
