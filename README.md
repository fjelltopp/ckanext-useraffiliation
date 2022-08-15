![tests](https://github.com/fjelltopp/ckanext-useraffiliation/actions/workflows/test.yml/badge.svg)  ![test coverage](https://coveralls.io/repos/fjelltopp/ckanext-useraffiliation/badge.svg)


# ckanext-useraffiliation

This CKAN extension add:

* job title; and
* affiliation

to the CKAN user schema displaying these fields in:

* registration form;
* user edit form; and
* user profile tile.


# Requirements
This extension is tested with CKAN 2.9 for python3 only.


# Installation

To install ckanext-useraffiliation:

1. Activate your CKAN virtual environment, for example:
   ```
   . /usr/lib/ckan/default/bin/activate
   ```

2. Install the ckanext-useraffiliation Python package into your virtual environment::
   ```
   pip install ckanext-useraffiliation
   ```

3. Add ``useraffiliation`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:
   ```
   sudo service apache2 reload
   ```


# Configuration


Ensure you have read and completed step 4 of the *Installation* section above.  This step is essential CKAN configuration required for this plugin to work.

There are no configuration options for this plugin.


# Running the Tests

To run the tests, do::

    pytest --ckan-ini=test.ini


# Releasing a New Version of ckanext-useraffiliation


ckanext-useraffiliation is availabe on PyPI as https://pypi.python.org/pypi/ckanext-useraffiliation.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist bdist_wheel

3. Upload the source distribution to PyPI::

     python -m twine upload dist/*

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   1.0.0 then do::

       git tag 1.0.0
       git push --tags



# With thanks...


This extension has been built by Fjelltopp with funding from UNAIDS as part of
the AIDS Data Repository project: [https://adr.unaids.org](https://adr.unaids.org)
