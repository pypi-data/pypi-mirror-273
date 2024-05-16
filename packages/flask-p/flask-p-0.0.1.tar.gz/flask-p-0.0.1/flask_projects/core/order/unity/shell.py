import click


@click.command('shell')
def shell():

    import code

    code.interact()
