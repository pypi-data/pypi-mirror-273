import click
from cli.utils.helm import Helm




@click.command(name='upgrade',context_settings=dict(ignore_unknown_options=True))
@click.argument('release_name',type=click.types.STRING,required=True)
@click.argument('chart_path',type=click.Path(exists=True),required=True)
@click.option('--values','-f',help=f"Provide values file path",type=click.Path(exists=True),multiple=True)
@click.option('--context','-c',help="Context that you want to use",type=click.STRING)
@click.option('--namespace','-n',help="Namespace you want to use",type=click.STRING)
@click.option('--no-validation',is_flag=True,help="If enabled skips validation for test helm branch")
def diff_upgrade(chart_path,release_name,values,context,namespace,no_validation):
    '''Show a diff explaining what a helm upgrade would change.'''
    helm=Helm(context=context,namespace=namespace)
    no_validation and click.echo("Skipping validation for test helm branch")
    no_validation or click.echo("Validating charts...")
    validation=no_validation or helm.validate_chart(chart_path)
    if validation is not True:
        return click.echo(validation)
    output=helm.diff(release_name,chart_path,values)
    click.echo(output)

