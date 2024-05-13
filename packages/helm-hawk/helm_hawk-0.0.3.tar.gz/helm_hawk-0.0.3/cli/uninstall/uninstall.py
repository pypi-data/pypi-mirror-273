import click
from cli.utils.helm  import Helm

@click.command(name='uninstall',help="This command takes a release name and uninstalls the release.")
@click.argument('release_name',type=click.STRING,required=True)
@click.option('--context','-c',help="Context that you want to use",type=click.STRING)
@click.option('--namespace','-n',help="Namespace you want to use",type=click.STRING)
@click.option('--dry-run',help="Simulate the upgrade",is_flag=True)
def uninstall_command(release_name,context,namespace,dry_run):
    """Uninstalls a helm release"""
    helm=Helm(namespace=namespace,context=context)
    output=helm.uninstall(release_name,dry_run)
    click.echo(output)


