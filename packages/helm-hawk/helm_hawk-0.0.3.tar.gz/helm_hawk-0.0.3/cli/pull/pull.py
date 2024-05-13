import click
from cli.utils.helm import Helm


@click.command(name="pull",help="Retrieve a package from a package repository, and download it locally.")
@click.argument('chart_name',type=click.STRING,required=True)
@click.option('--version',type=click.STRING,help="specify a version constraint for the chart version to use. This constraint can be a specific tag (e.g. 1.1.1) or it may reference a valid range (e.g. ^2.0.0). If this is not specified, the latest version is used")
@click.option('--username',type=click.STRING,help="chart repository username where to locate the requested chart")
@click.option('--password',type=click.STRING,help="chart repository password where to locate the requested chart")
@click.option('--untar',is_flag=True,help="if set to true, will untar the chart after downloading it")
@click.option('--repo',type=click.STRING,help="chart repository url where to locate the requested chart")
@click.option('--pass-credentials',is_flag=True,help="pass credentials to all domains")
def pull_command(chart_name,version,username,password,untar,repo,pass_credentials):
    '''Retrieve a package from a package repository, and download it locally.
    This is useful for fetching packages to inspect, modify, or repackage. It can
    also be used to perform cryptographic verification of a chart without installing
    the chart.'''
    helm=Helm(None,None)
    output=helm.pull(chart_name,version,username,password,untar,repo,pass_credentials)
    return click.echo(output)