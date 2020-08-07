# Vermont Police Tools - Tools for cleaning Vermont police data
#
# Written in 2020 by BTV CopWatch <info@btvcopwatch.org>
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Tools for cleaning University of Vermont Police Services data."""

import pandas as pd
from .. import utils


def clean_roster(csv):
    """Clean a digitized roster."""

    @utils.nullable
    def clean_star_no(star_no):
        assert star_no[:2] == "U-"
        return int(star_no[2:])

    @utils.nullable
    def clean_job_title(job_title):
        job_title_choices = {
            "Interim Chief": "Chief",
            "Deputy Chief": "Deputy Chief",
            "Sergeant": "Sergeant",
            "Police Officer": "Officer",
        }
        return job_title_choices[job_title]

    @utils.nullable
    def clean_race(race):
        race_choices = {
            "W": "WHITE",
        }
        return race_choices[race]

    dirty = pd.read_csv(csv)
    cleaned = pd.DataFrame()
    cleaned["job_title"] = dirty["Title"].apply(clean_job_title)
    cleaned["last_name"] = dirty["Last Name"]
    cleaned["first_name"] = dirty["First Name"]
    cleaned["middle_initial"] = dirty["MI"].apply(utils.clean_middle_initial)
    cleaned["star_no"] = dirty["Call Sign"].apply(clean_star_no)
    cleaned["employment_date"] = dirty["Date Hired"].apply(pd.to_datetime)
    cleaned["race"] = dirty["Race"].apply(clean_race)
    cleaned["gender"] = dirty["Gender"]
    cleaned["birth_year"] = dirty["Birthdate"]
    return cleaned
