raw_alternative_areas = [
    {
        "is_continental": False,
        "name": "Democrats Abroad",
        "is_obsolete": False,
        "capital": None,
        "ap_abbr": "Democrats Abroad",
        "time_zones": None,
        "fips": None,
        "abbr": "Democrats Abroad",
        "statehood_year": None,
        "is_contiguous": False,
        "capital_tz": None,
        "is_territory": False,
        "slug": "democrats-abroad",
    }
]


class ElectoralArea(object):
    repr_label = "ElectoralArea"

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

        try:
            import jellyfish

            self.__dict__["name_metaphone"] = jellyfish.metaphone(
                self.__dict__["name"]
            )
        except:
            pass

    def __repr__(self):
        return "<{}: {}>".format(self.repr_label, self.__str__())

    def __str__(self):
        return self.name


alternative_areas = dict(
    (area.get("slug").lower(), ElectoralArea(**area))
    for area in raw_alternative_areas
)
