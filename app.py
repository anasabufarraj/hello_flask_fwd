# ------------------------------------------------------------------------------
#  Copyright (c) 2020. Anas Abu Farraj.
# ------------------------------------------------------------------------------
"""Learning along Reading Flask Web Development Second Edition.

[ ]: TODO: Add Documentation.
[ ]: TODO: Add type notations.
[ ]: TODO: Migrate my app from single-script.
[ ]: TODO: Never guess, add ... or 'hard to guess secret'.
[√]: Store data in database.
"""

import click
from flask_migrate import Migrate
from application import create_app, db
from application.models import User, Role

app = create_app('default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context() -> dict:
    variables = dict(db=db, User=User, Role=Role)
    return variables


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names: str) -> None:
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    app.run(debug=True)
