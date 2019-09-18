import os
import pickle
import csv
from datetime import datetime

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
        if not obj[key] or type(obj[key]) != "str":
            continue
        if obj[key].lower() == "false":
            obj[key] = False
        if obj[key].lower() == "true":
            obj[key] = True
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


def pickle_seats():
    for YEAR in YEARS:
        seats = []
        seat_dir = os.path.join(ELECTIONS_DIR, YEAR, "seats")
        jurisdiction = ""
        for path, dirs, files in os.walk(seat_dir):
            if len(dirs) == 0:
                for file in files:
                    seat_type = file.replace(".csv", "")
                    seats_data = read_csv_to_dict(os.path.join(path, file))
                    for seat in seats_data:
                        seat = cast_types(seat)
                        seat["jurisdiction"] = jurisdiction
                        seat["seat_type"] = seat_type
                        seats.append(seat)
                jurisdiction = ""
            else:
                jurisdiction = dirs[0]

        os.makedirs(os.path.join(PKL_DIR, YEAR), exist_ok=True)
        with open(
            os.path.join(PKL_DIR, "{}/seats.pkl".format(YEAR)), "wb"
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
    pickle_seats()
    pickle_elections()


if __name__ == "__main__":
    pickle_data()
