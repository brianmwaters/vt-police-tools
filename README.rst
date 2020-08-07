Vermont Police Tools
====================

Tools for cleaning Vermont police data
--------------------------------------

This package contains miscellaneous tools for working with Vermont police data.
It was created to enable the addition of several police departments to
`OpenOversight <https://www.openoversight.com/>`_.

Data
~~~~

See `data <vt_police_tools/data/>`_.

Installation
~~~~~~~~~~~~

.. code:: sh

    pip install vt-police-tools

OpenOversight data import
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: sh

    cd vt_police_tools/
    ./migrations/2020.8-initial.sh

Development
~~~~~~~~~~~

.. code:: sh

    git clone https://github.com/brianmwaters/vt-police-tools.git
    cd vt-police-tools/
    virtualenv --python=python3.7 env/
    source env/bin/activate
    pip install --requirement requirements.txt
    pip install --editable .

Contributing
~~~~~~~~~~~~

Before submitting a patch, please lint your code by running ``pycodestyle`` and
``pydocstyle`` in the root directory, and ``shellcheck`` on all shell scripts.
Please make sure to also `test <tests/>`_ your code.
