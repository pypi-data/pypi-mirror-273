pytest_pt: pytest plugin to use `*.pt` files as tests
=====================================================

This [pytest] plugin will collect `*.pt` files as test modules. It
uses a custom module loader that always uses importlib (like specifying
`importmode=importlib` to the standard pytest loader) and generates
a module name ending in `~pt` to prevent namespace collisions.

Use this by deposting the [`pylib/pytest_pt.py`][pytest_pt] in any
directory where it will be found as the code for a (top-level) module, and
import it in a [`conftest.py`][conftest] in one or more directories under
which you want to collect `*.pt` files:

    from pytest_pt import *     # Plugin to find/execute .pt files as tests


Versions Supported
------------------

This supports only pytest 5, 7 and 8; pytest 6 doesn't seem worth
supporting because we have no legacy users of it. (This could be added if
there is any demand for it.)

- Python 3.6 probably works, but is not tested due to tox being unhappy
  about using it.
- pytest 5 is supported on versions of Python up to 3.9, but not on 3.10
  and above.
- pytest 7 and 8 are tested on Pythons up to 3.12, and will probably work
  on newer versions of Python when they are released.


Testing
-------

The top-level `./Test` script runs tests for all supported versions of
Python and pytest. You do not need `tox` installed (or even `pip` or
`virtualenv`); the script will take care of bootstrapping those into a
local virtualenv using [pactivate].

The script installs and uses [pythonz] to supply the various versions of
Python this is tested with. You should run it the first time with `-B`
as the first option to `./Test` to install/update pythonz and build
the versions of Python that tox will need to run the tests. (The
tests are for each minor release from 3.7 to 3.12; pythonz will be
asked to build the latest patch release for each of those.)

The test script could be updated to use Pythons from other sources, if
there is any call for it.

#### Tox Arguments

Any command line arguments given to `./Test` (with the exception of an
initial `-B`—see above) will be passed on to `tox`. So, e.g., `./Test -h`
will make tox print its help message. Typical arguments you might want to
pass through `./Test` to `tox` include: use include:

- `run -h`: Print help for the `tox run` command.

- `-a`: Print a list of all environments in the default list to be tested.
  This can be useful for finding an envirionment name for use in the `run`
  command below.

- `run -e py3.11-pytest8`: Run just a specific tox environment (or multiple
  ones separated by commas) rather than all environment.

- `config`: Print the tox configuration.


Release Process
---------------

This is described in [`mc68-net/r8format:doc/release.md`][rel] on GitHub.


Further Documentation
---------------------

This documentation should be expanded to explain more about the purpose of
this, how it works, and how the tests (run with `./Test`) work. Contact the
author if you're needing further documentation or help: Curt J. Sampson
<cjs@cynic.net>.



<!-------------------------------------------------------------------->
[conftest]: ./pylib/conftest.py
[pactivate]: https://github.com/cynic-net/pactivate
[pytest]: https://pytest.org/
[pytest_pt]: ./pylib/pytest_pt.py
[pythonz]: https://github.com/saghul/pythonz
[rel]: https://github.com/mc68-net/r8format/blob/main/doc/release.md
