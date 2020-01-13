# Imports from us-elections.
from elections.utils.alternative_areas import alternative_areas


# Imports from other dependencies.
import us


class PrimaryElection(object):
    is_runoff = False
    repr_label = "PrimaryElection"

    def __init__(self, **kwargs):
        if self.is_runoff:
            date_field = "runoff_election_date"
        else:
            date_field = "election_date"

        for k, v in kwargs.items():
            if k == "state":
                state_object = us.states.lookup(v)
                self.__dict__[k] = (
                    state_object
                    if state_object is not None
                    else alternative_areas[v.lower()]
                )
            elif k == "election_notes":
                self.__dict__[k] = v
            elif k == date_field:
                self.__dict__["election_date"] = v
            elif k != date_field and k.endswith("election_date"):
                pass
            else:
                self.__dict__[k] = v

    def __repr__(self):
        return "<{}: {}>".format(self.repr_label, self.__str__())

    def __str__(self):
        return "{} ({:%b. %d, %Y})".format(self.state.name, self.election_date)


class DemocraticPrimaryElection(PrimaryElection):
    repr_label = "DemocraticPrimaryElection"


class RepublicanPrimaryElection(PrimaryElection):
    repr_label = "RepublicanPrimaryElection"
