import click
from cli.utils.helm import Helm


@click.command(name="template",help="Render chart templates locally and display the output")
@click.argument('release_name',type=click.STRING,required=True)
@click.argument('chart_path', type=click.Path(exists=True),required=True)
@click.option("--values", "-f", multiple=True, help="Specify values in a YAML file (can specify multiple)")
@click.option('--context','-c',help="Context that you want to use",type=click.STRING)
@click.option('--namespace','-n',help="Namespace you want to use",type=click.STRING)
def template_command(context,namespace,release_name,chart_path,values):
    '''Render chart templates locally and display the output.
    Any values that would normally be looked up or retrieved in-cluster will be
    faked locally. Additionally, none of the server-side testing of chart validity
    (e.g. whether an API is supported) is done.'''
    helm=Helm(context,namespace)
    result = helm.helm_template(release_name=release_name,chart_path=chart_path,values=values)
    if result:
        return click.echo(result)