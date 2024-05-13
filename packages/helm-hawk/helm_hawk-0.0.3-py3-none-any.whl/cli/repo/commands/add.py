import click
from cli.utils.helm import Helm

@click.command(name="add",help="add a chart repository")
@click.argument("NAME",required=True)
@click.argument("URL",required=True)
@click.option('--pass-credentials',is_flag=True,help="pass credentials to all domains")
@click.option('--username',type=click.STRING,help="chart repository username where to locate the requested chart")
@click.option('--password',type=click.STRING,help="chart repository password where to locate the requested chart")
def add_command(name,url,pass_credentials,username,password):
    helm=Helm(None,None)
    output=helm.repo_add(name,url,pass_credentials,username,password)
    return click.echo(output)
