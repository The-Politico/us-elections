# Imports from other dependencies.
import us


class GeneralElection(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k == "state":
                self.__dict__[k] = us.states.lookup(v)
            else:
                self.__dict__[k] = v

    def __repr__(self):
        return "<GeneralElection: {}>".format(self.__str__())

    def __str__(self):
        return "{} ({:%b. %d, %Y})".format(self.state.name, self.election_date)
