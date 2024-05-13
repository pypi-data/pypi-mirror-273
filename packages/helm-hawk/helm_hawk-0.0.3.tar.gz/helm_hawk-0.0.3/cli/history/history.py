import click
from cli.utils.helm import Helm

@click.command(name="history")
@click.argument('release_name',type=click.STRING,required=True)
@click.option('--max',type=click.INT,default=255,help="maximum number of revision to include in history (default 256)")
@click.option('--context','-c',help="Context that you want to use",type=click.STRING)
@click.option('--namespace','-n',help="Namespace you want to use",type=click.STRING)
def history_command(max,release_name,context,namespace):
    """Commands related to the history of changes in a project."""
    helm = Helm(context=context,namespace=namespace)
    history=helm.history(release_name,max)
    click.echo(history)
    

