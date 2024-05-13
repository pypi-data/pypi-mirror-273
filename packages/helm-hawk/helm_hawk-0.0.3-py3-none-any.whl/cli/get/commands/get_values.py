import click
import subprocess


@click.command(name='values')
@click.argument('release_name',required=True,type=str)
@click.option('--context','-c',help="Context that you want to use",type=click.STRING)
@click.option('--namespace','-n',help="Namespace you want to use",type=click.STRING)
def get_values(release_name,context,namespace):
    '''Fetches values for a specific release'''
    if context:
        get_values_command=["helm",
                            "get",
                            "values",
                            release_name,
                            "--kube-context",
                            context]
    else:
        get_values_command = ["helm", 
                              "get", 
                              "values", 
                              release_name]
    
    if namespace:
        get_values_command.extend(["-n", namespace])


    subprocess.run(get_values_command)
