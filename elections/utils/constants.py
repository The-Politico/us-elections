# The first Presidential election was held in 1788, and such elections
# have been held every four years since.
FIRST_PRESIDENTIAL_ELECTION = 1788
PRESIDENTIAL_ELECTION_INTERVAL = 4


# Years at the "top" of a cycle are "presidential years".
# Years at the "bottom" of a cycle are "midterm years."
# We have placeholders to describe the other (odd-numbered) years, but
# we could stand to have better descriptors for these.
PRESIDENTIAL_YEAR_TYPE = "presidential"
ODD_YEAR_ONE_TYPE = "odd-year-1"
MIDTERM_YEAR_TYPE = "midterm"
ODD_YEAR_TWO_TYPE = "odd-year-3"

ELECTION_YEAR_TYPES = [
    PRESIDENTIAL_YEAR_TYPE,
    ODD_YEAR_ONE_TYPE,
    MIDTERM_YEAR_TYPE,
    ODD_YEAR_TWO_TYPE,
]
