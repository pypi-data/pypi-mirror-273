import click
from cli.utils.helm import Helm


@click.command("list",help="This command lists all of the releases for a specified namespace (uses current namespace context if namespace not specified).")
# @click.command("ls",help="This command lists all of the releases for a specified namespace (uses current namespace context if namespace not specified).")
@click.option("-a","--all",help="show all releases without any filter applied",is_flag=True)
@click.option("-A","--all-namespaces",help="list releases across all namespaces",is_flag=True)
@click.option('--context','-c',help="Context that you want to use",type=click.STRING)
@click.option('--namespace','-n',help="Namespace you want to use",type=click.STRING)
def list_command(all,all_namespaces,context,namespace):
    '''This command lists all of the releases for a specified namespace (uses current namespace context if namespace not specified).'''
    helm=Helm(context,namespace)
    output=helm.helm_list(all,all_namespaces)
    return click.echo(output)
