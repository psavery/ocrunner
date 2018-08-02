import click
import os
import subprocess

@click.group(help='ocrunner',
             context_settings=dict(help_option_names=['-h', '--help']))
def main():
  pass

# Cluster command
@main.group('cluster', short_help='Get information about the cluster.', help='Get information about the cluster.')
def cluster():
  pass

@click.command('ls', short_help='List available clusters.', help='List available clusters.')
def cluster_ls():
  print('Cluster ls called!')

cluster.add_command(cluster_ls)


# Jobs command
@main.group('jobs', short_help='Get information about the jobs.', help='Get information about the jobs.')
def jobs():
  pass

@click.command('ls', short_help='List running jobs.', help='List running jobs.')
def jobs_ls():
  print('Jobs ls called!')

jobs.add_command(jobs_ls)


# Taskflows command
@main.group('taskflows', short_help='Get information about the taskflows.', help='Get information about the taskflows.')
def taskflows():
  pass

@click.command('ls', short_help='List running taskflows.', help='List running taskflows.')
def taskflows_ls():
  print('taskflows ls called!')

taskflows.add_command(taskflows_ls)

if __name__ == '__main__':
  main()
