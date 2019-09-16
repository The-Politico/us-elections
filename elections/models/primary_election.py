import us


class PrimaryElection(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k == "state":
                self.__dict__[k] = us.states.lookup(v)
            else:
                self.__dict__[k] = v

    def __repr__(self):
        return "<PrimaryElection:%s>" % self.name

    def __str__(self):
        return self.name
