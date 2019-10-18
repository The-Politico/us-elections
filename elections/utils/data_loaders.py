# Imports from python.
from pkg_resources import resource_stream


# Imports from us-elections.
from elections.constants import DATA_MODULE_PATH


def load_pickled_data(pickled_file):
    return resource_stream(DATA_MODULE_PATH, pickled_file)
