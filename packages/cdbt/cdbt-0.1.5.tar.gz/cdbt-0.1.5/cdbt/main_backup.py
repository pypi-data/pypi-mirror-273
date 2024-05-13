import subprocess
import sys
import shutil
import os
from typing import List

import click


# Create a Click group
@click.group()
def cdbt():
    """cdbt is a CLI tool to manage dbt builds and handle states."""
    pass


@cdbt.command()
@click.option('--full-refresh', is_flag=True, help='Run a full refresh on all models.')
@click.option('--select', type=str, help='DBT style select string')
@click.option('--fail-fast', is_flag=True, help='Fail fast on errors.')
def build(full_refresh, select, fail_fast):
    args = []
    if select:
        args.append('--select')
        args.append(select)
    if fail_fast:
        args.append('--fail-fast')
    print(f'Starting a dbt build with args: {args}')
    try:
        execute_dbt_command('seed', args)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)

    run_args = args
    if full_refresh:
        run_args.append('--full-refresh')
    try:
        execute_dbt_command('seed', run_args)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)

    try:
        execute_dbt_command('test', args)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)


@cdbt.command()
@click.option('--full-refresh', is_flag=True, help='Run a full refresh on all models.')
@click.option('--select', type=str, help='DBT style select string')
@click.option('--fail-fast', is_flag=True, help='Fail fast on errors.')
def run(full_refresh, select, fail_fast):
    args = []
    if select:
        args.append('--select')
        args.append(select)
    if fail_fast:
        args.append('--fail-fast')

    run_args = args
    if full_refresh:
        run_args.append('--full-refresh')
    try:
        execute_dbt_command('seed', run_args)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)


@cdbt.command()
def compile(full_refresh, select, fail_fast):
    try:
        subprocess.run(['dbt', 'compile'], check=True)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)


@cdbt.command()
@click.option('--full-refresh', is_flag=True, help='Run a full refresh on all models.')
def sbuild(full_refresh):
    print('Starting a state build based on local manifest.json')
    artifact_dir = '_artifacts'
    target_dir = 'target'
    # Path to the artifacts file that will be generated by the dbt compile command representing the current state.
    manifest_path = os.path.join('./', target_dir, 'manifest.json')
    # Path to the backup file to create in case of an error.
    manifest_backup_path = os.path.join('./', artifact_dir, 'manifest.json_bak')
    # Path to the artifact file that represents the prior build state.
    manifest_artifact_path = os.path.join('./', artifact_dir, 'manifest.json')

    execute_state_based_build(artifact_dir, manifest_artifact_path, manifest_backup_path, manifest_path, full_refresh,
                              roll_back_manifest_flag=True)


@cdbt.command()
@click.option('--full-refresh', is_flag=True, help='Run a full refresh on all models.')
def pbuild(full_refresh):
    print('Starting a state build based on production manifest.json')
    artifact_dir = 'logs'
    target_dir = 'target'
    # Pull artifacts from Snowflake. These are the latest production artifacts.
    try:
        subprocess.run(['dbt', 'run-operation', 'get_last_artifacts'], check=True)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)

    manifest_path = os.path.join('.', target_dir, 'manifest.json')
    manifest_backup_path = os.path.join('.', artifact_dir, 'manifest.json_bak')
    manifest_artifact_path = os.path.join('.', artifact_dir, 'manifest.json')

    execute_state_based_build(artifact_dir, manifest_artifact_path, manifest_backup_path, manifest_path, full_refresh,
                              roll_back_manifest_flag=False)


def execute_state_based_build(artifact_dir: str, manifest_artifact_path: str, manifest_backup_path: str,
                              manifest_path: str, full_refresh: bool, roll_back_manifest_flag: bool):
    print(f'Pulling manifest from {manifest_artifact_path}')
    if roll_back_manifest_flag:
        # Backup and move manifest.json. Only used for local state build. Not used for pdbuild (production build).
        # First move the current manifest to the backup location
        shutil.copy(manifest_artifact_path, manifest_backup_path)
        #
        shutil.move(manifest_path, manifest_artifact_path)
    # Execute dbt compile
    try:
        subprocess.run(['dbt', 'compile'], check=True)
    except subprocess.CalledProcessError:
        # Rollback if dbt compile fails
        shutil.move(manifest_artifact_path, manifest_path)
        shutil.move(manifest_backup_path, manifest_artifact_path)
        sys.exit(1)
    # Construct state commands
    state_flags = [
        '--select', 'state:modified+',
        '--state', os.path.join('.', artifact_dir) + '/'
    ]

    # Execute dbt seed
    try:
        execute_dbt_command('seed', state_flags)
    except subprocess.CalledProcessError as e:
        if roll_back_manifest_flag:
            roll_back_manifest(e, manifest_artifact_path, manifest_backup_path, manifest_path)
        else:
            print(e)
            sys.exit(1)

    # Execute dbt run
    if full_refresh:
        run_flags = state_flags + ['--full-refresh']
    else:
        run_flags = state_flags
    try:
        execute_dbt_command('run', run_flags)
    except subprocess.CalledProcessError as e:
        if roll_back_manifest_flag:
            roll_back_manifest(e, manifest_artifact_path, manifest_backup_path, manifest_path)
        else:
            print(e)
            sys.exit(1)

    # Execute dbt test
    try:
        execute_dbt_command('test', state_flags)
    except subprocess.CalledProcessError as e:
        if roll_back_manifest_flag:
            roll_back_manifest(e, manifest_artifact_path, manifest_backup_path, manifest_path)
        else:
            print(e)
            sys.exit(1)


def roll_back_manifest(e, manifest_artifact_path, manifest_backup_path, manifest_path):
    print(f"DBT build failed. Rolling back manifest state with error\n {e}")
    shutil.move(manifest_artifact_path, manifest_path)
    shutil.move(manifest_backup_path, manifest_artifact_path)
    sys.exit(1)


def execute_dbt_command(command: str, args: List[str]):
    command = ['dbt', command] + args
    print(f'Running command: {command}')
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)


if __name__ == "__main__":
    sbuild()
