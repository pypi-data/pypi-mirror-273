import click
from cli.utils.helm import Helm

@click.command(name='status')
@click.argument('release_name',type=click.STRING)
@click.option('--context','-c',help="Context that you want to use",type=click.STRING)
@click.option('--namespace','-n',help="Namespace you want to use",type=click.STRING)
@click.option('--revision',help="if set, display the status of the named release with revision",type=click.STRING)
@click.option('--output','-o',type=click.STRING,help="prints the output in the specified format. Allowed values: table, json, yaml (default table)")
@click.option('--show-desc',help="if set, display the description message of the named release",is_flag=True)
def status_command(release_name, show_desc,revision,output,context,namespace):
    '''This command shows the status of a named release.
    The status consists of:
    - last deployment time
    - k8s namespace in which the release lives
    - state of the release (can be: unknown, deployed, uninstalled, superseded, failed, uninstalling, pending-install, pending-upgrade or pending-rollback)
    - revision of the release
    - description of the release (can be completion message or error message, need to enable --show-desc)
    - list of resources that this release consists of (need to enable --show-resources)
    - details on last test suite run, if applicable
    - additional notes provided by the chart'''
    helm=Helm(context=context,namespace=namespace)
    output=helm.status(release_name,show_desc,revision,output)
    click.echo(output)
