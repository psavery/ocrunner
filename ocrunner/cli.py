import click
import os
import sys

import girder_client
from girder_client import HttpError

from ocrunner.utilities.clusters_utils import ClustersUtils
from ocrunner.utilities.user_utils import UserUtils
from ocrunner.utilities.progress_bar import progress_bar

DEFAULT_API_URL = 'http://localhost:8080/api/v1'


def getClient(apiUrl, apiKey):
    """Get an authenticated GirderClient object.

    Takes an apiUrl and an apiKey and returns an authenticated
    girder_client.GirderClient object.

    If the apiUrl is empty or set to "None", the environment variable
    "OCRUNNER_API_URL" will be used. If it is not set, the
    default http://localhost:8080/api/v1 value will be used instead.

    If the apiKey is empty or set to "None", the environment variable
    "OCRUNNER_API_KEY" will be used. A valid api key is mandatory.
    """
    if not apiUrl:
        apiUrl = os.getenv('OCRUNNER_API_URL')
        if not apiUrl:
            apiUrl = DEFAULT_API_URL

    if not apiKey:
        apiKey = os.getenv('OCRUNNER_API_KEY')
        if not apiKey:
            sys.exit('An api key is required to run this script. '
                     'See --help for more info')

    progress_bar.reportProgress = sys.stdout.isatty()

    gc = girder_client.GirderClient(apiUrl=apiUrl,
                                    progressReporterCls=progress_bar)

    try:
        gc.authenticate(apiKey=apiKey)
    except HttpError as e:
        if e.status == 500:
            print('Error: invalid api key')
            return None

        raise
    except Exception as e:
        print('Failed to connect to server.')
        print('\nThe following error occurred:\n', e)
        return None

    return gc


@click.group(help='ocrunner',
             context_settings=dict(help_option_names=['-h', '--help']))
@click.option(
    '--api-url',
    help=('The girder api url. May also set OCRUNNER_API_URL environment '
          'variable.'))
@click.option(
    '--api-key',
    help=('The girder api key. May also set OCRUNNER_API_KEY environment '
          'variable.'))
@click.pass_context
def main(ctx, api_url, api_key):
    gc = getClient(api_url, api_key)
    ctx.obj = dict()
    ctx.obj['gc'] = gc


# Cluster command
@main.group(
    'cluster',
    short_help='Get information about the cluster.',
    help='Get information about the cluster.')
@click.pass_context
def cluster(ctx):
    pass


@click.command(
    'ls',
    short_help='List available clusters.',
    help='List available clusters.')
@click.pass_context
def cluster_ls(ctx):
    gc = ctx.obj['gc']
    clustersList = ClustersUtils(gc).clusters()
    print('=' * 44)
    print('{:15s} {:12s} {:15s}'.format('host', 'status', 'user'))
    print('=' * 44)
    for cluster in clustersList:
        userId = cluster['userId']
        user = UserUtils(gc).getUserLogin(userId)
        print(
            '{:15s} {:12s} {:15s}'.format(
                cluster['config']['host'],
                cluster['status'],
                user))


cluster.add_command(cluster_ls)


# Jobs command
@main.group('jobs', short_help='Get information about the jobs.',
            help='Get information about the jobs.')
@click.pass_context
def jobs(ctx):
    pass


@click.command(
    'ls',
    short_help='List running jobs.',
    help='List running jobs.')
@click.pass_context
def jobs_ls(ctx):
    print('Jobs ls called!')


jobs.add_command(jobs_ls)


# Taskflows command
@main.group(
    'taskflows',
    short_help='Get information about the taskflows.',
    help='Get information about the taskflows.')
@click.pass_context
def taskflows(ctx):
    pass


@click.command(
    'ls',
    short_help='List running taskflows.',
    help='List running taskflows.')
@click.pass_context
def taskflows_ls(ctx):
    print('taskflows ls called!')


taskflows.add_command(taskflows_ls)

if __name__ == '__main__':
    main()
