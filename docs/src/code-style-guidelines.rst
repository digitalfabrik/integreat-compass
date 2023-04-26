*********************
Code Style Guidelines
*********************

We use `pre-commit-hooks <https://pre-commit.com/>`_ to apply style formatters before committing, so you don't have to bother about formatting.
Just code how you feel comfortable and let the tool do the work for you (see :ref:`pre-commit-hooks`).

.. _black-code-style:

Black
-----

We use the `black <https://github.com/psf/black>`_ coding style, a flavour of `PEP-8 <https://www.python.org/dev/peps/pep-0008/>`_ for Python.

Run black manually by starting the virtual environment and then:

    black .

Pylint
-------

In addition to black, we use pylint to check the code for semantic correctness.

When you think a warning is a false positive, add a comment before the specific line::

    # pylint: disable=unused-argument
    def some_function(*args, **kwargs)

.. Note::

    Please use the string identifiers (``unused-argument``) instead of the alphanumeric code (``W0613``) when disabling warnings.

Prettier
--------

We use `prettier <https://github.com/prettier/prettier>`_ as the code formatter for JS/TS, CSS, HTML, JSON, YAML and Markdown.

Tell prettier to format your code by running:

    npx prettier . --write

or use

    npx prettier . --check

to only check for violations without fixing them.

Eslint
------

Just as with pylint for python code, we use eslint to check JS/TS code for semantic correctness.

False positive warnings can be ignored by adding a comment before the offending line::

    /* eslint-disable-next-line no-console */
    console.log("something important")
