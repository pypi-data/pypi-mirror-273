import click 
from cli.utils.helm import Helm


@click.command(name="remove",help="remove one or more chart repositories")
@click.argument("REPO",nargs=-1)
def remove_command(repo):
    helm=Helm(None,None)
    output=helm.repo_remove(repo)
    return click.echo(output)