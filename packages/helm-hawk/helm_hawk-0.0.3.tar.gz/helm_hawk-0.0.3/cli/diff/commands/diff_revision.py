import click
from cli.utils.helm import Helm





@click.command(name='revision')
@click.argument('release_name',type=click.STRING,required=True)
@click.argument('old_revision',type=click.STRING,required=True)
@click.argument('new_revision',type=click.STRING,required=True)
@click.option('--context','-c',help="Context that you want to use",type=click.STRING)
@click.option('--namespace','-n',help="Namespace you want to use",type=click.STRING)
def diff_revison(release_name,old_revision,new_revision,context,namespace):
    '''
    Show a diff of a specific revision against the last known one.
    '''
    helm=Helm(namespace=namespace,context=context)
    output=helm.diff_revison(release_name=release_name,old_revision=old_revision,new_revision=new_revision)
    click.echo(output)