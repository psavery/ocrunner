"""The taskflows commands."""

import click
import json
import logging

from ocrunner.utilities.taskflows_utils import TaskflowsUtils


@click.command(
    'ls',
    short_help='List running taskflows.',
    help='List running taskflows.')
@click.option('--all', is_flag=True, default=False)
@click.pass_context
def taskflows_ls(ctx, all):
    gc = ctx.obj['gc']

    if all:
      taskflowsList = TaskflowsUtils(gc).listAllTaskflows()
    else:
      taskflowsList = TaskflowsUtils(gc).listTaskflows()

    print('=' * 100)
    print('{:28s} {:12s} {:60s}'.format('id', 'status', 'TaskFlowClass'))
    print('=' * 100)
    for taskflow in taskflowsList:
        print(
            '{:28s} {:12s} {:60s}'.format(
                taskflow['_id'],
                taskflow['status'],
                taskflow['taskFlowClass']))


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


@click.command(
    'start',
    short_help='Start a taskflow with a given id.',
    help='Start a taskflow with a given id.')
@click.argument('taskflowId')
@click.argument('inputJsonFile')
@click.pass_context
def taskflows_start(ctx, taskflowid, inputjsonfile):
    gc = ctx.obj['gc']

    # Read the input file
    with open(inputjsonfile, 'r') as rf:
        body = json.load(rf)

    print('Starting task flow:', taskflowid)
    resp = TaskflowsUtils(gc).startTaskflow(taskflowid, body)


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
        record = logging.makeLogRecord(log)
        print(logging.Formatter().format(record))
        logCount += 1
    print('**** Done printing log ****')


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


@click.command(
    'jobs',
    short_help='List the jobs for a given taskflow.',
    help='List the jobs for a given taskflow.')
@click.argument('taskflowId')
@click.pass_context
def taskflows_jobs(ctx, taskflowid):
    gc = ctx.obj['gc']

    taskFlowInfo = TaskflowsUtils(gc).getTaskflow(taskflowid)

    # The jobs are in the meta data
    metaData = taskFlowInfo.get("meta")
    if not metaData:
        print("Error: meta data not present in taskflow!")
        return

    jobsList = metaData.get("jobs")
    print('=' * 68)
    print('{:28s} {:20s} {:30s}'.format('jobId', 'name', 'status'))
    print('=' * 68)
    for job in jobsList:
        print(
            '{:28s} {:20s} {:30s}'.format(
                job['_id'],
                job['name'],
                job['status']))
