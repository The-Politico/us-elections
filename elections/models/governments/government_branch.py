# Imports from other dependencies.
import us
from us.states import State as StateKlass


# Imports from us-elections.
from elections.models.governments.constants import BRANCHES
from elections.utils.builts import ChamberFilterableList


class GovernmentBranch(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k == "branch_type" and v in BRANCHES:
                self.type = v
            elif k == "seats":
                if v:
                    self.__dict__[k] = v
            else:
                self.__dict__[k] = v

    @property
    def jurisdiction_name(self):
        return self.jurisdiction.__dict__["name"]

    @property
    def jurisdiction_abbreviation(self):
        return self.jurisdiction.__dict__["ap_abbr"]

    @property
    def verbose_name(self):
        if hasattr(self, "body_name"):
            if self.jurisdiction_abbreviation == "U.S.":
                return "{} {}".format(
                    self.jurisdiction_abbreviation, self.body_name
                )
            return "{} {}".format(self.jurisdiction_name, self.body_name)
        return self.jurisdiction_name

    @property
    def is_empty(self):
        return not hasattr(self, "seats")

    def count_seats(self):
        if self.is_empty:
            return 0
        else:
            return len(self.seats)

    def __repr__(self):
        return "<{}Branch: {}>".format(
            self.type.capitalize(), self.verbose_name
        )

    def __str__(self):
        if self.verbose_name != self.jurisdiction_name:
            return "{} ({} {} Branch)".format(
                self.verbose_name,
                self.jurisdiction_abbreviation,
                self.type.capitalize(),
            )
        return "{} {} Branch".format(
            self.jurisdiction_abbreviation, self.type.capitalize()
        )


class LegislativeBranch(GovernmentBranch):
    def __init__(self, **kwargs):
        super(LegislativeBranch, self).__init__(**kwargs)

        if not isinstance(self.jurisdiction, StateKlass):

            def get_seats_for_state(state):
                state = us.states.lookup(state)
                return ChamberFilterableList(
                    [seat for seat in self.seats if seat.state == state]
                )

            self.seats_for_state = get_seats_for_state


class ExecutiveBranch(GovernmentBranch):
    @property
    def chief(self):
        if self.count_seats():
            return self.seats.chief
        return None
