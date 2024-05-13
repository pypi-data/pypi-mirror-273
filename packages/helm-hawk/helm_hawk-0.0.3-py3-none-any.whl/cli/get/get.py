import click
from cli.get.commands.get_values import get_values


@click.group(name='get')
def get_group():
    '''Group of commands  to retrieve information from the server'''
    pass




get_group.add_command(get_values)