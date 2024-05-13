import click
from cli.diff import diff_group
from cli.get import get_group
from cli.history import history_command
from cli.status import status_command
from cli.rollback import rollback_command
from cli.upgrade import upgrade_command
from cli.uninstall import uninstall_command
from cli.list import list_command
from cli.template import template_command
from cli.pull import pull_command
from cli.repo import repo_group
@click.group()
@click.option('--context','-c',help="Name of the context you want to use",type=click.STRING,is_flag=True)
@click.option('--namespace','-n',help="Namespace for which you want to see the resources.",type=click.STRING,is_flag=True)
def  cli(context,namespace):
    '''Wrapper for helm'''
    pass






cli.add_command(diff_group)
cli.add_command(get_group)
cli.add_command(repo_group)
cli.add_command(history_command)
cli.add_command(status_command)
cli.add_command(rollback_command)
cli.add_command(upgrade_command)
cli.add_command(uninstall_command)
cli.add_command(list_command)
cli.add_command(template_command)
cli.add_command(pull_command)
if __name__=="__main__":
    cli()