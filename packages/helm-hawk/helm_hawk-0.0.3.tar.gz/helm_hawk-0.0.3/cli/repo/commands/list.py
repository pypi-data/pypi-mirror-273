import click
from cli.utils.helm import Helm

@click.command(name="list",help="list chart repositories")
@click.option("-o","--output",type=click.STRING,help="prints the output in the specified format. Allowed values: table, json, yaml (default table)")
def list_command(output):
    helm=Helm(None,None)
    output=helm.repo_list(output)
    return click.echo(output)
