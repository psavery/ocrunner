"""The clusters commands."""

import click

from ocrunner.utilities.clusters_utils import ClustersUtils
from ocrunner.utilities.user_utils import UserUtils


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
