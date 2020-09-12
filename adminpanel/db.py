import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def init_app(app):
    # closing any previous connections
    app.teardown_appcontext(close_db)
    #registering the init-db flask command
    app.cli.add_command(init_db_cmd)
    


def init_db():
    db = get_db()

    with current_app.open_instance_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


@click.command('init-db')
@with_appcontext
def init_db_cmd():
    """ Defining a flask command to 
        clear existing tables and create new
    """
    init_db()
    click.echo('Initialized db.')

def get_db():
    """
        This methods checks for an existing db connection
        and returns if it exists else creates a new connection
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
