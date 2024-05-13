import click
from cli.utils.helm import Helm


@click.command(name="upgrade",help="This command upgrades a release to a new version of a chart.")
@click.argument('release_name',type=click.STRING,required=True)
@click.argument('chart_path', type=click.Path(exists=True),required=True)
@click.option("--values", "-f", multiple=True, help="Specify values in a YAML file (can specify multiple)")
@click.option('--context','-c',help="Context that you want to use",type=click.STRING)
@click.option('--namespace','-n',help="Namespace you want to use",type=click.STRING)
@click.option('--dry-run',help="Simulate the upgrade",is_flag=True)
@click.option('--no-validation',is_flag=True,help="If enabled skips validation for test helm branch")
def upgrade_command(release_name,chart_path,values,context,namespace,dry_run,no_validation):
    helm=Helm(namespace=namespace,context=context)
    no_validation or click.echo("Validating Chart...")
    validation=no_validation or helm.validate_chart(chart_path)
    no_validation and click.echo("Skipping validation for test helm branch")
    if no_validation: proceed=input("You are about to upgrade a release with no validations. Do you want to proceed? (yes/no): ")
    if no_validation and proceed.lower() != "yes":
        return click.echo("Aborting")
    if validation is not True:
        return click.echo(validation)
    output=helm.diff(release_name,chart_path,values)
    click.echo(output)
    prompt=input("enter Yes to perform the upgrade: ")
    if prompt.lower() == "yes":
        output=helm.upgrade(release_name,chart_path,values,False)
        click.echo(output)

