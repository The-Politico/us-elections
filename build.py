# Imports from python.
import csv
from datetime import datetime
import os
import pickle


# Imports from other dependencies.
import us


PWD = os.path.abspath(os.path.dirname(__file__))
DB = os.path.join(PWD, "db")
ELECTIONS_DIR = os.path.join(DB, "elections")
PKL_DIR = os.path.join(PWD, "elections/data/")

# GET YEARS
YEARS = list(os.walk(ELECTIONS_DIR))[0][1]


def read_csv_to_dict(path):
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def cast_dates(obj):
    for key in obj:
        if (key[-5:] == "_date" or key[-9:] == "_deadline") and obj[key]:
            obj[key] = datetime.strptime(obj[key], "%Y-%m-%d")
    return obj


def cast_bools(obj):
    for key in obj:
        if type(obj[key]) == str:
            if obj[key].lower() == "false":
                obj[key] = False
                return obj
            if obj[key].lower() == "true":
                obj[key] = True
                return obj
    return obj


def cast_nulls(obj):
    for key in obj:
        if obj[key] == "":
            obj[key] = None
    return obj


def cast_types(obj):
    obj = cast_nulls(obj)
    obj = cast_bools(obj)
    obj = cast_dates(obj)
    return obj


def pickle_parties():
    parties = [
        cast_types(party)
        for party in read_csv_to_dict(os.path.join(DB, "parties/parties.csv"))
    ]
    with open(os.path.join(PKL_DIR, "parties.pkl"), "wb") as pkl_file:
        pickle.dump(parties, pkl_file, protocol=2)


def pickle_years():
    with open(os.path.join(PKL_DIR, "years.pkl"), "wb") as pkl_file:
        pickle.dump(YEARS, pkl_file, protocol=2)


def pickle_electoral_votes():
    for YEAR in YEARS:
        vote_zones = []
        electoral_votes_for_year = os.path.join(
            ELECTIONS_DIR, YEAR, "electoral-votes.csv"
        )

        if os.path.exists(electoral_votes_for_year):
            votes_data = read_csv_to_dict(electoral_votes_for_year)
            for vote_zone in votes_data:
                vote_zone = cast_types(vote_zone)
                vote_zone["type"] = (
                    "by-district" if vote_zone["district"] else "statewide"
                )
                vote_zones.append(vote_zone)

        os.makedirs(os.path.join(PKL_DIR, YEAR), exist_ok=True)
        with open(
            os.path.join(PKL_DIR, "{}/electoral-votes.pkl".format(YEAR)), "wb"
        ) as pkl_file:
            pickle.dump(vote_zones, pkl_file, protocol=2)


def pickle_seats_for_body(government_level, chosen_branch):
    if isinstance(government_level, str):
        government_level = [government_level]

    for YEAR in YEARS:
        seats = []
        seat_dir_for_level = os.path.join(
            ELECTIONS_DIR, YEAR, "seats", *government_level
        )

        for path, dirs, files in os.walk(seat_dir_for_level):
            path_parts = path.split(os.path.sep)
            level_components = path_parts[-len(government_level) :]

            if len(dirs) == 0 and chosen_branch == path_parts[-1]:
                for file in files:
                    seat_type = file.replace(".csv", "")
                    seats_data = read_csv_to_dict(os.path.join(path, file))
                    for seat in seats_data:
                        seat = cast_types(seat)
                        seat["jurisdiction"] = "/".join(government_level)
                        seat["seat_type"] = seat_type
                        seats.append(seat)
            elif len(dirs) == 0 and level_components == government_level:
                branch_singleton_file = None
                for file in files:
                    file_name = file.replace(".csv", "")
                    if file_name == chosen_branch:
                        branch_singleton_file = file

                if branch_singleton_file:
                    seats_data = read_csv_to_dict(
                        os.path.join(path, branch_singleton_file)
                    )
                    for seat in seats_data:
                        seat = cast_types(seat)
                        seat["jurisdiction"] = "/".join(government_level)
                        seats.append(seat)
                else:
                    pass
            else:
                pass

        os.makedirs(os.path.join(PKL_DIR, YEAR), exist_ok=True)
        with open(
            os.path.join(
                PKL_DIR,
                "{}/{}-{}-seats.pkl".format(
                    YEAR, government_level[-1], chosen_branch
                ),
            ),
            "wb",
        ) as pkl_file:
            pickle.dump(seats, pkl_file, protocol=2)


def pickle_elections():
    for YEAR in YEARS:
        elections = []
        election_dir = os.path.join(ELECTIONS_DIR, YEAR, "calendars")
        jurisdiction = ""
        for path, dirs, files in os.walk(election_dir):
            if len(dirs) == 0:
                for file in files:
                    election_type = file.replace(".csv", "")
                    elections_data = read_csv_to_dict(os.path.join(path, file))
                    for election in elections_data:
                        election = cast_types(election)
                        election["jurisdiction"] = jurisdiction
                        election["election_type"] = election_type
                        elections.append(election)
                jurisdiction = ""
            else:
                jurisdiction = dirs[0]

        os.makedirs(os.path.join(PKL_DIR, YEAR), exist_ok=True)
        with open(
            os.path.join(PKL_DIR, "{}/elections.pkl".format(YEAR)), "wb"
        ) as pkl_file:
            pickle.dump(elections, pkl_file, protocol=2)


def pickle_data():
    pickle_parties()
    pickle_years()

    pickle_electoral_votes()

    pickle_seats_for_body("federal", "legislative")
    pickle_seats_for_body("federal", "executive")

    for state in us.STATES:
        if state.statehood_year:  # Taxation w/o representation! Nix D.C.
            pickle_seats_for_body(["state", state.abbr.lower()], "legislative")
            pickle_seats_for_body(["state", state.abbr.lower()], "executive")
            pickle_seats_for_body(["state", state.abbr.lower()], "judicial")

    pickle_elections()


if __name__ == "__main__":
    pickle_data()
