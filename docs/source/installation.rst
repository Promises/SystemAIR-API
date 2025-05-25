Installation
============

From PyPI
---------

The recommended way to install SystemAIR-API is from PyPI:

.. code-block:: bash

    pip install systemair-api

From Source
-----------

You can also install from source if you want the latest development version:

.. code-block:: bash

    git clone https://github.com/promises/SystemAIR-API.git
    cd SystemAIR-API
    pip install -e .

For Development
--------------

If you're planning to contribute to the project, install with development dependencies:

.. code-block:: bash

    pip install -e ".[dev]"

Additionally, you should set up pre-commit hooks:

.. code-block:: bash

    pre-commit install

Requirements
-----------

SystemAIR-API requires:

* Python 3.7+
* requests
* websocket-client
* beautifulsoup4
* python-dotenv