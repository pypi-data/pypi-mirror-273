# Tempy

![coverage report](https://gitlab.com/topf-lab/tempy/badges/master/coverage.svg)

## Installation (For Development)

Python 3.7 is recommended, although python 3.5+ should be supported but not tested.
The Tempy environment assumes Python 3.7 will be used, this can be changed in
the `Pipfile`

`Pipenv` is required which creates the virtual environment and can be installed via
`pip`:

> pip install pipenv

Ensure you have Python 3.7 installed on your machine.

To install the required packages you first need to enter the shell of the
virtual environment :

> pipenv shell

and then install the packages with:

> pipenv install --dev

All the required packages should now be installed

## Development

#### Guidelines on contributing

Please do all work in a feature branch based off the `develop` branch.
Once they're done, send a merge request and it will be merged into `develop`,
pending a review (and provided all tests pass).

Don't forget to run `flake8` on your codebase to check for code quality. If
any errors are detected it will not be merged into the `develop` branch.

Please write tests!

Also, consider running pylint and/or black before you submit merge requests.

#### Test

You need to install pytest to run the test suites.
To run tests, run `pytest` in the top directory.



#### Releases

Releases are handled with `bumpversion`, this should be used to handle all git tagging
and automated versioning for TEMPy. Versioning of TEMPy has the following schema:

- Development releases: `{major}.{minor}.{patch}-{release}.{build}`
- Production releases: `{major}.{minor}.{patch}`

The `{release}` element of the schema has the following values:
- alpha
- beta
- rc
- prod

When creating a new major version the version tag will default to:
`[major release number].0.0-alpha.0` 

To iterate through the release value a new release must be released as follows:

> bumpversion release

The version will now become `[major release number].0.0-beta.0`. Doing another release
will then iterate to `rc`. If this is done again the is now a `prod` release (a version 
released to PyPi) so the version will me `[major release number].0.0`

Example usages:

> bumperversion major

Current version `2.0.0` will change to `3.0.0-alpha.0`

> bumpversion build

Current version `3.0.0-alpha.0` will change to `3.0.0-alpha.1`

> bumpversion minor

Current version `3.0.0-alpha.1` will change to `3.1.0-alpha.0`

> bumpversion patch

Current version `3.1.0-alpha.1` will change to `3.1.1-alpha.0`

> bumpversion release

Current version `3.1.1-alpha.0` will change to `3.1.1-beta.0`

> bumpversion release

Current version `3.1.1-beta.0` will change to `3.1.1-rc.0`

> bumpversion release

Current version `3.1.1-rc.0` will change to `3.1.1`

The version `3.1.1` is the version released to production!

Generally, the release tags indicate the state of the software:
- `alpha`: code in a bad state, lots of process breaking bugs, lots of bugs. This would be the `develop` branch
- `beta`: code in a good state, few process breaking bugs, bugs. This would be the `develop` branch
- `rc`: code in a very good state, tests pass, no know process breaking bugs, no known bugs or bugs are small. This would be the `release` branch
- `prod`: Code is release worthy and ready to be launched to PyPi. This is `master` branch

