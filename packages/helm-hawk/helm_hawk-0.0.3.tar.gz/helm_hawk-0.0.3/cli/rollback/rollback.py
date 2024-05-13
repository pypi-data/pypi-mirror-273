import click
from cli.utils.helm import Helm



@click.command(name="rollback",help="This command rolls back a release to a previous revision.")
@click.argument('release_name',type=click.STRING,required=True)
@click.argument('revision',type=click.STRING,required=True)
@click.option('--context','-c',help="Context that you want to use",type=click.STRING)
@click.option('--namespace','-n',help="Namespace you want to use",type=click.STRING)
@click.option('--dry-run',help="simulate a rollback",is_flag=True)
@click.option('--no-hooks',help="prevent hooks from running during rollback",is_flag=True)
def rollback_command(release_name,namespace,context,dry_run,no_hooks,revision):
    '''This command rolls back a release to a previous revision.

    The first argument of the rollback command is the name of a release, and the
    second is a revision (version) number. If this argument is omitted or set to
    0, it will roll back to the previous release.

    To see revision numbers, run 'helm history RELEASE'.
    '''
    helm=Helm(context=context,namespace=namespace)
    output=helm.rollback(release_name,revision,dry_run,no_hooks)
    click.echo(output)

