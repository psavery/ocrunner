"""The jobs commands."""

import click

from ocrunner.utilities.jobs_utils import JobsUtils


@click.command(
    'ls',
    short_help='List running jobs.',
    help='List running jobs.')
@click.pass_context
def jobs_ls(ctx):
    gc = ctx.obj['gc']
    jobsList = JobsUtils(gc).listJobs()
    print('=' * 68)
    print('{:28s} {:20s} {:30s}'.format('jobId', 'name', 'status'))
    print('=' * 68)
    for job in jobsList:
        print(
            '{:28s} {:20s} {:30s}'.format(
                job['_id'],
                job['name'],
                job['status']))
