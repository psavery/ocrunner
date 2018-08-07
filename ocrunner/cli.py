import click
import json
import os
import sys

import girder_client
from girder_client import HttpError

from ocrunner.utilities.progress_bar import progress_bar

from ocrunner.clusters import commands as clusters_commands
from ocrunner.jobs import commands as jobs_commands
from ocrunner.taskflows import commands as taskflows_commands

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


# Clusters command
@main.group(
    'clusters',
    short_help='Run commands for the clusters.',
    help='Run commands for the clusters.')
@click.pass_context
def clusters(ctx):
    pass

clusters.add_command(clusters_commands.clusters_ls)


# Jobs command
@main.group('jobs', short_help='Run commands for the jobs.',
            help='Run commands for the jobs.')
@click.pass_context
def jobs(ctx):
    pass

jobs.add_command(jobs_commands.jobs_ls)


# Taskflows command
@main.group(
    'taskflows',
    short_help='Get information about the taskflows.',
    help='Get information about the taskflows.')
@click.pass_context
def taskflows(ctx):
    pass

taskflows.add_command(taskflows_commands.taskflows_ls)
taskflows.add_command(taskflows_commands.taskflows_create)
taskflows.add_command(taskflows_commands.taskflows_start)
taskflows.add_command(taskflows_commands.taskflows_terminate)
taskflows.add_command(taskflows_commands.taskflows_delete)
taskflows.add_command(taskflows_commands.taskflows_log)
taskflows.add_command(taskflows_commands.taskflows_status)
taskflows.add_command(taskflows_commands.taskflows_jobs)

if __name__ == '__main__':
    main()
