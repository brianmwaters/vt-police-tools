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

source migrations/common

function import {
	add_dept 'Burlington Police Department' BPD
	add_jobs 'Not Sure' Officer Corporal Sergeant Lieutenant \
		'Deputy Chief' Chief
	bulk_add --update-by-name bpd 2019-05 non-union-seniority-list
	bulk_add --update-by-name bpd 2019-05 bpoa-seniority-list
	bulk_add '--update-by-name --update-static-fields' bpd 2020-01 \
		non-union-seniority-list
	bulk_add --update-by-name bpd 2020-01 bpoa-seniority-list
	bulk_add --update-by-name bpd 2020-07 part-time-officer-list
	bulk_add '--no-create --update-by-name' bpd 2019-06 demographics
	bulk_add '--no-create --update-by-name --update-static-fields' bpd \
		2020-01 demographics
	bulk_add '--no-create --update-by-name' bpd 2019-06 annual-report
	bulk_add '--no-create --update-by-name' bpd 2020-07 departures

	add_dept 'UVM Police Services' UVMPS
	add_jobs 'Not Sure' Officer Sergeant 'Deputy Chief' Chief
	bulk_add --update-by-name uvmps 2020-01 roster

	add_dept "Chittenden County Sheriff's Office" CCSO
	add_jobs 'Not Sure' Deputy Corporal Sergenat Lieutenant Captain Sheriff
	bulk_add --update-by-name ccso 2020-01 roster

	add_dept 'Vermont Capitol Police' VCP
	add_jobs 'Not Sure' Officer Sergeant Chief
	bulk_add --update-by-name vcp 2020-04 roster
}

log import
