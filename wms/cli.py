"""This is a script which is run when the WMS package is executed."""
import errno
import os

import click
import streamlit.cli as _st_cli

from wms.hello import demo as _demo

OUTPUT_DIR = os.path.expanduser(os.path.join("~", ".wms"))
DATABASE_DIR = os.path.join(OUTPUT_DIR, "database")
SECURITY_KEY = os.path.join(OUTPUT_DIR, ".encryption_key")
DATABASE_FILE = os.path.join(DATABASE_DIR, "WMS.db")


def _create_output_dir():
    """Creates the output directory for database and encryption key."""
    from wms import encryption

    check = False
    if not os.path.exists(DATABASE_DIR):
        try:
            os.makedirs(DATABASE_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        else:
            check = True

    if not os.path.exists(SECURITY_KEY):
        encryption.hash_password(SECURITY_KEY)
        check = True

    return check


@click.group()
@click.option("--set-password", "--setup", "--set", is_flag=True)
@click.pass_context
def main(ctx, set_password):
    """Try out a demo with:

        $ wms hello
    """

    from wms import encryption

    need_new_password = _create_output_dir()
    if need_new_password and not set_password:
        if click.confirm("This is the first time you run this demo, do you want to set a new password?"):
            set_password = True
        else:
            click.secho("\nApp will be launched with the default password [python].", fg="green")

    if set_password:
        password = click.prompt("\nPassword", default="python", hide_input=True, confirmation_prompt=True)
        if password == "python":
            if click.confirm("Continue with the default password?", default=True, abort=True):
                pass
        encryption.hash_password(SECURITY_KEY, password)


@main.command("hello")
@click.pass_context
def main_hello(ctx):
    """Executes when run `wms hello`."""
    import sys

    filename = _demo.__file__
    sys.argv = ["streamlit", "run", filename]
    sys.exit(_st_cli.main())
