# Imports from other dependencies.
import us


supt_verbose = "Superintendent of Public Instruction"

EXECUTIVE_OFFICE_NAMES = {
    "president": "President",
    "vice-president": "Vice President",
    "governor": "Governor",
    "lieutenant-governor": "Lieutenant Governor",
    "secretary-of-state": "Secretary of State",
    "superintendent-of-public-instruction": supt_verbose,
    "attorney-general": "Attorney General",
    "auditor": "Auditor",
    "treasurer": "Treasurer",
    "agriculture-commissioner": "Commissioner of Agriculture",
    "labor-commissioner": "Commissioner of Labor",
    "insurance-commissioner": "Insurance Commissioner",
    "commissioner-of-public-lands": "Commissioner of Public Lands",
}


class ExecutiveSeat(object):
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
    def office_verbose(self):
        return EXECUTIVE_OFFICE_NAMES.get(self.office, "Unknown office")

    def __repr__(self):
        return "<ExecutiveSeat: {}>".format(self.__str__())

    def __str__(self):
        if self.is_federal:
            return "U.S. {}".format(self.office_verbose)
        else:
            return "{} {}".format(self.state.name, self.office_verbose)


class HeadOfGovernmentSeat(ExecutiveSeat):
    head_of_government = True
