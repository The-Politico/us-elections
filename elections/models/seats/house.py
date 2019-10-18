# Imports from other dependencies.
import us


# Imports from us-elections.
from elections.utils.formatters import ordinalize


class HouseSeat(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k == "state":
                self.__dict__[k] = us.states.lookup(v)
            else:
                self.__dict__[k] = v

    @property
    def is_federal(self):
        return self.jurisdiction == "federal"

    @property
    def is_at_large(self):
        return not self.district

    @property
    def district_name(self):
        if self.is_at_large:
            return "at-large district"
        return "{} district".format(ordinalize(int(self.district)))

    def __repr__(self):
        return "<HouseSeat: {}>".format(self.__str__())

    def __str__(self):
        if self.is_federal:
            return "{} U.S. House seat, {}".format(
                self.state.name, self.district_name
            )
        else:
            return "{} state house seat, {}".format(
                self.state.name, self.district_name
            )
