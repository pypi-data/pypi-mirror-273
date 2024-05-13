import click
from cli.repo.commands.add import add_command
from cli.repo.commands.list import list_command
from cli.repo.commands.update import update_command
from cli.repo.commands.remove import remove_command



@click.group(name="repo",help="This command consists of multiple subcommands to interact with chart repositories.")
def repo_group():
    '''
    This command consists of multiple subcommands to interact with chart repositories.
    It can be used to add, remove, list, and index chart repositories.

    Usage:
    helm repo [command]

    Available Commands:
    add         add a chart repository
    index       generate an index file given a directory containing packaged charts
    list        list chart repositories
    remove      remove one or more chart repositories
    update      update information of available charts locally from chart repositories
    '''
    pass


repo_group.add_command(add_command)
repo_group.add_command(list_command)
repo_group.add_command(update_command)
repo_group.add_command(remove_command)