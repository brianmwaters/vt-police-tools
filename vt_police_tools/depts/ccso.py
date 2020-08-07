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

"""Tools for cleaning Chittenden County Sheriff's Office data."""

import pandas as pd
from .. import utils


def clean_roster(csv):
    """Clean a digitized roster."""

    @utils.nullable
    def clean_job_title(job_title):
        job_title_choices = {
            "Sheriff": "Sheriff",
            "Captain": "Captain",
            "Lieutenant": "Lieutenant",
            "Sergeant": "Sergeant",
            "Corporal": "Corporal",
            "Deputy": "Deputy",
            "Deuty": "Deputy",  # Fix a typo.
        }
        return job_title_choices[job_title]

    @utils.nullable
    def clean_star_no(star_no):
        assert star_no[:2] == "CC"
        return int(star_no[2:])

    @utils.nullable
    def clean_employment_date(employment_date):
        return pd.to_datetime(employment_date.replace(".", "/"))

    @utils.nullable
    def clean_race(race):
        race_choices = {
            "B": "BLACK",
            "W": "WHITE",
        }
        return race_choices[race.capitalize()]

    @utils.nullable
    def clean_gender(gender):
        return gender.capitalize()

    dirty = pd.read_csv(csv)
    # Get the year from the name of the rightmost column.
    salary_label = dirty.columns[-2]
    overtime_pay_label = dirty.columns[-1]
    salary_year = int(salary_label.split()[-1])
    cleaned = pd.DataFrame()
    cleaned["job_title"] = dirty["Rank"].apply(clean_job_title)
    names = dirty["Full Name"].apply(utils.clean_full_name)
    # middle_initial and suffix aren't in the data, but they're returned by
    # clean_full_name, so we drop them.
    names = names.drop(["middle_initial", "suffix"], axis=1)
    cleaned = pd.concat([cleaned, names], axis=1)
    cleaned["star_no"] = dirty["Badge Number - "].apply(clean_star_no)
    cleaned["employment_date"] = \
        dirty["Hire Date"].apply(clean_employment_date)
    cleaned["race"] = dirty["Race"].apply(clean_race)
    cleaned["gender"] = dirty["Gender"].apply(clean_gender)
    cleaned["birth_year"] = dirty["Year of Birth"]
    cleaned["salary"] = dirty[salary_label].apply(utils.clean_salary)
    cleaned["overtime_pay"] = \
        dirty[overtime_pay_label].apply(utils.clean_salary).fillna(0)
    cleaned["salary_year"] = salary_year
    cleaned["salary_is_fiscal_year"] = False
    return cleaned
