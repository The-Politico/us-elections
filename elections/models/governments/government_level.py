# Imports from other dependencies.
import us


# Imports from us-elections.
from elections.models.governments.government_branch import ExecutiveBranch
from elections.models.governments.government_branch import GovernmentBranch
from elections.models.governments.government_branch import LegislativeBranch
from elections.models.governments.constants import BRANCHES
from elections.models.governments.constants import LEGISLATIVE
from elections.models.governments.constants import EXECUTIVE


class GovernmentLevel(object):
    jurisdiction = None

    verbose_class_name = "Government"

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k in BRANCHES:
                if k == EXECUTIVE:
                    branch_klass = ExecutiveBranch
                else:
                    branch_klass = GovernmentBranch

                self.__dict__[k] = branch_klass(
                    branch_type=k, jurisdiction=self.jurisdiction, seats=v
                )

            else:
                self.__dict__[k] = v

    def get_verbose_class_name(self):
        return self.verbose_class_name

    def __repr__(self):
        return "<{}: {}>".format(self.get_verbose_class_name(), self.__str__())

    def __str__(self):
        return getattr(self.jurisdiction, "name", "Undefined")

    @property
    def abbreviation(self):
        return self.jurisdiction.__dict__.get("ap_abbr", "??")


class StateGovernment(GovernmentLevel):
    verbose_class_name = "StateGovernment"


class FederalGovernment(GovernmentLevel):
    verbose_class_name = "FederalGovernment"

    def __init__(self, **kwargs):
        government_jurisdiction = kwargs.get("jurisdiction", self.jurisdiction)
        congress_seats = kwargs.pop(LEGISLATIVE, [])
        if congress_seats:
            self.__dict__[LEGISLATIVE] = LegislativeBranch(
                branch_type=LEGISLATIVE,
                jurisdiction=government_jurisdiction,
                seats=congress_seats,
                body_name="Congress",
            )

        raw_electoral_votes = kwargs.pop("electoral_votes", None)

        super(FederalGovernment, self).__init__(**kwargs)

        if self.legislative:
            self.congress = self.legislative

        if self.executive and not self.executive.is_empty:
            if raw_electoral_votes:
                self.executive.chief.electoral_votes = raw_electoral_votes

            self.president = self.executive.chief
        elif self.executive and self.executive.is_empty:
            self.president = None
