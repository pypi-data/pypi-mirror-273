import click
from cli.diff.commands import diff_upgrade
from cli.diff.commands import diff_revison


@click.group(name='diff')
def diff_group():
    '''Group of commands for comparing two versions of helm chart'''
    pass



diff_group.add_command(diff_upgrade)
diff_group.add_command(diff_revison)