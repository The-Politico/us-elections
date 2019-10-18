# Imports from other dependencies.
import us


class SenateSeat(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k == "state":
                self.__dict__[k] = us.states.lookup(v)
            else:
                self.__dict__[k] = v

    @property
    def is_federal(self):
        return self.jurisdiction == "federal"

    def __repr__(self):
        return "<SenateSeat: {}>".format(self.__str__())

    def __str__(self):
        if self.is_federal:
            return "{} U.S. Senate seat, class {}".format(
                self.state.name, self.senate_class
            )
        else:
            return "{} state senate seat, class {}".format(
                self.state.name, self.senate_class
            )
