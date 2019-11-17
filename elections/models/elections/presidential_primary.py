# Imports from other dependencies.
import us


class PresidentialPrimaryElection(object):
    party_prefix = None
    repr_label = "PresidentialPrimaryElection"

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k == "state":
                self.__dict__[k] = us.states.lookup(v)
            elif k == "election_notes":
                self.__dict__[k] = v
            elif self.party_prefix and k.startswith(self.party_prefix):
                self.__dict__[k[len(self.party_prefix) :]] = v

    def __repr__(self):
        return "<{}: {}>".format(self.repr_label, self.__str__())

    def __str__(self):
        return "{} {:%b. %d, %Y}".format(self.state.name, self.election_date)


class DemocraticPresidentialPrimaryElection(PresidentialPrimaryElection):
    party_prefix = "dem_"
    repr_label = "DemocraticPresidentialPrimaryElection"


class RepublicanPresidentialPrimaryElection(PresidentialPrimaryElection):
    party_prefix = "gop_"
    repr_label = "RepublicanPresidentialPrimaryElection"
