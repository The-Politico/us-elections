# Imports from us-elections.
from elections.models.elections import PrimaryElection


# Imports from other dependencies.
import us


class PrimaryRunoffElection(PrimaryElection):
    is_runoff = True
    repr_label = "PrimaryRunoffElection"


class DemocraticPrimaryRunoffElection(PrimaryRunoffElection):
    repr_label = "DemocraticPrimaryRunoffElection"


class RepublicanPrimaryRunoffElection(PrimaryRunoffElection):
    repr_label = "RepublicanPrimaryRunoffElection"
