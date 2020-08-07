This directory contains roster data from various police departments, for import
into `OpenOversight <https://www.openoversight.com/>`_. For each officer in each
department, we aim to have the following data:

- First name
- Last name
- Middle initial
- Suffix (such as "Jr.")
- Badge number
- Rank
- Unit assignment
- Hire date
- Race
- Gender
- Year of birth
- Salary
- Overtime pay
- Retirement date (if applicable)

We get this data via public records requests and published sources like agency
websites (see `sources <SOURCES.rst>`_), and our goal is to to update each
department biannually, since the Vermont Police Academy graduates two classes
per year.

Each subdirectory corresponds to a police department. Within each one, there are
subdirectories with a mont-wise date-stamp, like ``2019-05/``. Each of these
corresponds to a record or series of records obtained that month.

Within each date-stamped subdirectory, there are up to four subdirectories, with
names like ``raw/``, ``digitized/``, ``cleaned/``, and ``imported``. ``raw/``
contains the files we obtain via public records requests. Relevant sections from
each file are then converted to CSV files on an ad-hoc basis, and placed in
``digitized/``. This is done in such a way as to represent the original source
data as closely as possible. The resulting CSV files are then filtered and
cleaned using the `Pandas scripts <../>`_, and placed in ``cleaned/``. This
cleaned data is then imported into OpenOversight using the `migration scripts
<../migrations/>`_. These append a department ID column onto each CSV; the data
is then finally logged under ``imported/`` exactly as it is imported into
OpenOversight.
