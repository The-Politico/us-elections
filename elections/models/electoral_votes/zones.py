# Imports from other dependencies.
import us


# Imports from us-elections.
from elections.utils.formatters import ordinalize


class ElectoralZone(object):
    def __init__(self, **kwargs):
        self.is_federal = True

        for k, v in kwargs.items():
            if k == "state":
                self.__dict__[k] = us.states.lookup(v)
            elif k == "district" and v:
                self.__dict__[k] = v
            elif k == "elector_count":
                self.__dict__[k] = int(v)
            else:
                self.__dict__[k] = v

    @property
    def is_statewide(self):
        return not self.district

    @property
    def district_name(self):
        if self.is_statewide:
            return "statewide vote"
        return "{} district vote".format(ordinalize(int(self.district)))

    def __repr__(self):
        return "<ElectoralZone: {}>".format(self.__str__())

    def __str__(self):
        return "{} {}".format(self.state.name, self.district_name)


class DistrictElectoralZone(ElectoralZone):
    pass


class StateElectoralZone(ElectoralZone):
    pass
