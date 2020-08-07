#!/usr/bin/env bash

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

set -o errexit -o pipefail -o noglob

: "${DATA=./data/}"

function test_ {
	dept=${1}
	month=${2}
	csv=${3}

	digitized=${DATA}/${dept}/${month}/digitized/${csv}.csv
	cleaned=${DATA}/${dept}/${month}/cleaned/${csv}.csv

	if [[ -z "${4+x}" ]]
	then
		cmd="vpt ${dept} --${csv} ${digitized}"
	else
		cmd="vpt --year ${4} ${dept} --${csv} ${digitized}"
	fi

	echo "Testing ${dept} ${month} ${csv}"
	$cmd | diff "${cleaned}" -
}

test_ bpd 2019-05 non-union-seniority-list
test_ bpd 2019-05 bpoa-seniority-list
test_ bpd 2019-06 demographics
test_ bpd 2019-06 annual-report 2019
test_ bpd 2020-01 non-union-seniority-list
test_ bpd 2020-01 demographics
test_ ccso 2020-01 roster
test_ uvmps 2020-01 roster
test_ bpd 2020-01 bpoa-seniority-list
test_ vcp 2020-04 roster
test_ bpd 2020-07 part-time-officer-list
test_ bpd 2020-07 departures
