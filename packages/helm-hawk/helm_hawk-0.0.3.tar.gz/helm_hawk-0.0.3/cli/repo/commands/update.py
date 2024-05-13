import click
from cli.utils.helm import Helm

@click.command(name="update",help="Update gets the latest information about charts from the respective chart repositories.")
@click.argument("REPO",nargs=-1)
def update_command(repo):
    ''''''
    helm=Helm(None,None)
    output=helm.repo_update(repo)
    return click.echo(output)