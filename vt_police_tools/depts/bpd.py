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

"""Tools for cleaning Burlington Police Department data."""

import re

import numpy as np
import pandas as pd
from .. import utils


def correct_name(row):
    """Correct known misspelled names from the data."""
    if row["last_name"] == "Digiorgio" and row["first_name"] == "Kevin":
        row["last_name"] = "DiGiorgio"
    elif row["last_name"] == "Huynk" and row["first_name"] == "Nho":
        row["last_name"] = "Huynh"
    elif row["last_name"] == "Lacouture" and row["first_name"] == "Deidre":
        row["last_name"] = "LaCouture"
    elif row["last_name"] == "Nguyen" and row["first_name"] == "My":
        row["first_name"] = "My Thanh"
    elif row["last_name"] == "Winters" and row["first_name"] == "Luz":
        row["first_name"] = "Luz Maria"
    elif row["last_name"] == "Small" and row["first_name"] == "Phil":
        row["first_name"] = "Philip"
    return row


def clean_non_union_seniority_list(csv):
    """Clean a digitized non-union seniority list."""
    sworn_job_titles = [
        "Chief",
        "Deputy Chief",
        "Lieutenant",
        "Sergeant",
    ]

    dirty = pd.read_csv(csv)
    filtered = dirty[dirty["Rank/Title"].isin(sworn_job_titles)]
    clean = pd.DataFrame()
    clean["job_title"] = filtered["Rank/Title"]
    clean["last_name"] = filtered["Last Name"]
    clean["first_name"] = filtered["First Name"]
    clean = clean.apply(correct_name, axis=1)
    clean["star_no"] = filtered["Badge #"]
    clean["employment_date"] = \
        filtered["Original Date of Hire"].apply(pd.to_datetime)
    return clean


def clean_bpoa_seniority_list(csv):
    """Clean a digitized BPOA seniority list."""
    dirty = pd.read_csv(csv)
    clean = pd.DataFrame()
    clean["job_title"] = dirty["Rank"]
    clean["last_name"] = dirty["Last name"]
    clean["first_name"] = dirty["First Name"]
    clean = clean.apply(correct_name, axis=1)
    clean["star_no"] = dirty["Badge No."]
    clean["employment_date"] = dirty["Hire Date"].apply(pd.to_datetime)
    return clean


def clean_demographics(csv):
    """Clean a digitized demographics file."""

    @utils.nullable
    def clean_birth_year(birth_year):
        if type(birth_year) == str and birth_year[-1] == "-":
            birth_year = birth_year[:-1]
        return int(birth_year)

    @utils.nullable
    def clean_gender(gender):
        gender_choices = {
            "Female": "F",
            "Male": "M",
        }
        return gender_choices[gender]

    @utils.nullable
    def clean_race(race):
        race_choices = {
            "Asian": "ASIAN",
            "Black or African American": "BLACK",
            "Hispanic or Latino": "HISPANIC",
            "Two or More Races": "Not Sure",
            "White": "WHITE",
        }
        return race_choices[race]

    dirty = pd.read_csv(csv, header=None)
    # Data from some months has column headers, which we drop.
    if dirty.iat[0, 1] == "First Name":
        dirty = dirty.drop(0).reset_index(drop=True)
    clean = pd.DataFrame()
    clean["last_name"] = dirty[0]
    clean["first_name"] = dirty[1]
    clean = clean.apply(correct_name, axis=1)
    clean["race"] = dirty[4].apply(clean_race)
    clean["gender"] = dirty[3].apply(clean_gender)
    clean["birth_year"] = dirty[2].apply(clean_birth_year)
    return clean


def clean_annual_report(csv, year):
    """Clean a digitized annual report."""

    @utils.nullable
    def clean_name(name):
        # Remove star appended to names of employees w/ 20 years of service
        if name[-1] == '✧':
            unstarred_name = name[:-1]
        else:
            unstarred_name = name
        return utils.clean_full_name(unstarred_name)

    dirty = pd.read_csv(csv, header=None)
    clean = dirty[0].apply(clean_name)
    clean["salary"] = dirty[1].apply(utils.clean_salary)
    clean["salary_year"] = year
    clean["salary_is_fiscal_year"] = True
    return clean


def clean_part_time_officer_list(csv):
    """Clean a part-time officer list."""

    @utils.nullable
    def clean_name(name):
        clean = pd.Series()
        first_name, last_name = name.split(" ")
        clean["first_name"], clean["last_name"] = name.split(" ")
        return clean

    dirty = pd.read_csv(csv)
    clean = dirty["Name"].apply(clean_name)
    clean = clean.apply(correct_name, axis=1)
    clean["job_title"] = dirty["Rank"]
    clean["star_no"] = dirty["Badge"]
    clean["employment_date"] = dirty["Hire Date"].apply(pd.to_datetime)
    return clean


def clean_departures(csv):
    """Clean a departures list."""

    dirty = pd.read_csv(csv)
    clean = dirty["Name"].apply(utils.clean_full_name)
    # Drop fields not in the data
    clean = clean.drop(["middle_initial", "suffix"], axis=1)
    clean["resign_date"] = dirty["Date of departure"].apply(pd.to_datetime)
    return clean
