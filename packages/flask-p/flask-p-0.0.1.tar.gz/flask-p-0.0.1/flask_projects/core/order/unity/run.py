import click

from flask_projects.core.vars.application import application
from flask_projects.core.vars.info import info


@click.command('run')
def run():

    application.app.run(
        host=info.query('ip'),
        port=info.query('port'),
        *info.query('args'),
        **info.query('kwargs')
    )
