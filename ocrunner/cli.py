import click
import json
import os
import sys

import girder_client
from girder_client import HttpError

from ocrunner.utilities.clusters_utils import ClustersUtils
from ocrunner.utilities.taskflows_utils import TaskflowsUtils
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
    'clusters',
    short_help='Get information about the clusters.',
    help='Get information about the clusters.')
@click.pass_context
def clusters(ctx):
    pass


@click.command(
    'ls',
    short_help='List available clusters.',
    help='List available clusters.')
@click.pass_context
def clusters_ls(ctx):
    gc = ctx.obj['gc']
    clustersList = ClustersUtils(gc).clusters()
    print('=' * 72)
    print('{:15s} {:28s} {:12s} {:15s}'.format('host', 'id', 'status', 'user'))
    print('=' * 72)
    for cluster in clustersList:
        userId = cluster['userId']
        user = UserUtils(gc).getUserLogin(userId)
        print(
            '{:15s} {:28s} {:12s} {:15s}'.format(
                cluster['config']['host'],
                cluster['_id'],
                cluster['status'],
                user))


clusters.add_command(clusters_ls)


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

@click.command(
    'create',
    short_help='Create a taskflow from an input json file.',
    help='Create a taskflow from an input json file.')
@click.argument('inputJsonFile')
@click.pass_context
def taskflows_create(ctx, inputjsonfile):

    gc = ctx.obj['gc']

    # Read the input file
    with open(inputjsonfile, 'r') as rf:
        body = json.load(rf)

    resp = TaskflowsUtils(gc).createTaskflow(body)

    print('Taskflow created')
    print('id:', resp.get('_id'))
    print('status:', resp.get('status'))

taskflows.add_command(taskflows_create)

@click.command(
    'start',
    short_help='Start a taskflow with a given id.',
    help='Start a taskflow with a given id.')
@click.argument('taskflowId')
@click.pass_context
def taskflows_start(ctx, taskflowid):

    gc = ctx.obj['gc']

    print('Starting task flow:', taskflowid)
    resp = TaskflowsUtils(gc).startTaskflow(taskflowid)

taskflows.add_command(taskflows_start)

@click.command(
    'terminate',
    short_help='Terminate a taskflow with a given id.',
    help='Terminate a taskflow with a given id.')
@click.argument('taskflowId')
@click.pass_context
def taskflows_terminate(ctx, taskflowid):

    gc = ctx.obj['gc']

    print('Terminating task flow:', taskflowid)
    resp = TaskflowsUtils(gc).terminateTaskflow(taskflowid)

taskflows.add_command(taskflows_terminate)

@click.command(
    'delete',
    short_help='Delete a taskflow with a given id.',
    help='Delete a taskflow with a given id.')
@click.argument('taskflowId')
@click.pass_context
def taskflows_delete(ctx, taskflowid):

    gc = ctx.obj['gc']

    print('Deleting task flow:', taskflowid)
    resp = TaskflowsUtils(gc).deleteTaskflow(taskflowid)

taskflows.add_command(taskflows_delete)

@click.command(
    'log',
    short_help='Get the log of a taskflow with a given id.',
    help='Get the log of a taskflow with a given id.')
@click.argument('taskflowId')
@click.pass_context
def taskflows_log(ctx, taskflowid):

    gc = ctx.obj['gc']

    logCount = 1
    print('**** Printing log for taskflow', taskflowid, '****')
    resp = TaskflowsUtils(gc).log(taskflowid)
    for log in resp:
        print('*** Log entry:', logCount, '***')
        for entry in log.keys():
            print(entry, ":", log[entry])
        logCount += 1
    print('**** Done printing log ****')

taskflows.add_command(taskflows_log)

@click.command(
    'status',
    short_help='Get the status of a taskflow with a given id.',
    help='Get the status of a taskflow with a given id.')
@click.argument('taskflowId')
@click.pass_context
def taskflows_status(ctx, taskflowid):

    gc = ctx.obj['gc']

    status = TaskflowsUtils(gc).status(taskflowid)
    print('taskflow:', taskflowid)
    print('status:', status)

taskflows.add_command(taskflows_status)

if __name__ == '__main__':
    main()
