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

"""Utility functions."""

import functools
import re

import numpy as np
import pandas as pd


def nullable(func):
    """Decorate a function to handle null arguments."""
    @functools.wraps(func)
    def decorator(arg):
        if pd.isnull(arg):
            return arg
        else:
            return func(arg)
    return decorator


@nullable
def clean_full_name(full_name):
    """Split a full name into parts."""
    suffix_choices = {
        "Jr.": "JR",
        "Sr.": "SR",
        "II": "II",
        "III": "III",
        "IV": "IV",
        "V": "V",
    }
    pattern = (r"([\w'\s-]+), ([\w'\s-]+?)(?: (\w)(?:\.)?)?(?: ("
               + r"|".join(suffix_choices.keys())
               + r"))?")
    match = re.fullmatch(pattern, full_name)
    if match is not None:
        last, first, middle, suffix = match.groups()
    else:
        last, first, middle, suffix = np.nan, np.nan, np.nan, np.nan
    if not pd.isnull(suffix):
        suffix = suffix_choices[suffix]
    clean = pd.Series()
    clean["last_name"] = last
    clean["first_name"] = first
    clean["middle_initial"] = middle
    clean["suffix"] = suffix
    return clean


@nullable
def clean_middle_initial(middle):
    """Truncate a middle name or middle initial to a single capital letter."""
    middle_initial = middle[0].capitalize()
    if middle_initial.isalpha():
        return middle_initial.capitalize()
    else:
        return np.nan


@nullable
def clean_salary(salary):
    """Clean a dollar amount."""
    pattern = r"\$?(\d{1,3})(?:,(\d{3}))*(\.\d{2})?"
    match = re.fullmatch(pattern, salary)
    dollars = \
        int("".join([g for g in match.groups()[:-1] if g is not None]))
    if match.groups()[-1] is not None:
        cents = float(match.groups()[-1])
        return dollars + cents
    else:
        return dollars
