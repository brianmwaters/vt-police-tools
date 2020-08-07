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

"""Command-line interface for cleaning Vermont Police data."""

import argparse
import inspect
import sys

from . import __version__
from .depts import bpd
from .depts import ccso
from .depts import uvmps
from .depts import vcp


def _make_parser():
    parser = argparse.ArgumentParser(
        description=inspect.cleandoc(__doc__),
        epilog="example: vpt bpd --bpoa-seniority-list list.csv")
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=__version__)
    parser.add_argument("--year")
    commands = parser.add_subparsers(
        title="departments",
        dest="department",
        required=True)

    bpd = commands.add_parser(
        "bpd", description="Burlington Police Department")
    bpd_cleaners = bpd.add_mutually_exclusive_group(required=True)
    bpd_cleaners.add_argument("--bpoa-seniority-list", metavar="CSVFILE")
    bpd_cleaners.add_argument("--non-union-seniority-list", metavar="CSVFILE")
    bpd_cleaners.add_argument("--demographics", metavar="CSVFILE")
    bpd_cleaners.add_argument("--annual-report", metavar="CSVFILE")
    bpd_cleaners.add_argument("--part-time-officer-list", metavar="CSVFILE")
    bpd_cleaners.add_argument("--departures", metavar="CSVFILE")

    uvmps = commands.add_parser(
        "uvmps", description="University of Vermont Police Services")
    uvmps.add_argument("--roster", required=True, metavar="CSVFILE")

    ccso = commands.add_parser(
        "ccso", description="Chittenden County Sheriff's Office")
    ccso.add_argument("--roster", required=True, metavar="CSVFILE")

    vcp = commands.add_parser("vcp", description="Vermont Capitol Police")
    vcp.add_argument("--roster", required=True, metavar="CSVFILE")

    return parser


def main():
    """Run the command-line interface for this package."""
    parser = _make_parser()
    args = parser.parse_args()
    if args.department == "bpd":
        if args.bpoa_seniority_list is not None:
            cleaned = bpd.clean_bpoa_seniority_list(args.bpoa_seniority_list)
        elif args.non_union_seniority_list is not None:
            cleaned = bpd.clean_non_union_seniority_list(
                args.non_union_seniority_list)
        elif args.demographics is not None:
            cleaned = bpd.clean_demographics(args.demographics)
        elif args.annual_report is not None:
            if args.year is None:
                parser.print_usage(file=sys.stderr)
                print(
                    "error: --year is required with --annual-report",
                    file=sys.stderr)
                sys.exit(2)
            cleaned = bpd.clean_annual_report(args.annual_report, args.year)
        elif args.part_time_officer_list is not None:
            cleaned = bpd.clean_part_time_officer_list(
                args.part_time_officer_list)
        elif args.departures is not None:
            cleaned = bpd.clean_departures(args.departures)

    elif args.department == "uvmps":
        cleaned = uvmps.clean_roster(args.roster)

    elif args.department == "ccso":
        cleaned = ccso.clean_roster(args.roster)

    elif args.department == "vcp":
        cleaned = vcp.clean_roster(args.roster)

    cleaned.to_csv(sys.stdout, index=False)
    return 0
