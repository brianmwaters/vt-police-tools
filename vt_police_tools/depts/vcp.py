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

"""Tools for cleaning Vermont Capitol Police data."""

import pandas as pd
from .. import utils


def clean_roster(csv):
    """Clean a digitized roster."""
    dirty = pd.read_csv(csv, header=None)
    names = dirty[0].apply(utils.clean_full_name)
    # Drop suffix, which is not in the data
    names = names.drop("suffix", axis=1)
    clean = pd.concat([dirty[1], names, dirty[2]], axis=1)
    return clean.rename(columns={1: "job_title", 2: "star_no"})
