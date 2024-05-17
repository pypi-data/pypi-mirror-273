import click
import re

from cdbt.main import ColdBoreCapitalDBT
from cdbt.build_dbt_docs_ai import BuildDBTDocs
from cdbt.build_unit_test_data_ai import BuildUnitTestDataAI
cdbt_class = ColdBoreCapitalDBT()


# Create a Click group
class CustomCmdLoader(click.Group):

    def get_command(self, ctx, cmd_name):
        ctx.ensure_object(dict)

        # Match commands ending with + optionally followed by a number, such as 'sbuild+' or 'sbuild+3'
        suffix_match = re.match(r'(.+)\+(\d*)$', cmd_name)
        if suffix_match:
            cmd_name, count = suffix_match.groups()
            ctx.obj['build_children'] = True
            ctx.obj['build_children_count'] = int(count) if count else None  # Default to 1 if no number is specified

        # Match commands starting with a number followed by +, such as '3+sbuild'
        prefix_match = re.match(r'(\d+)\+(.+)', cmd_name)
        if prefix_match:
            count, cmd_name = prefix_match.groups()
            ctx.obj['build_parents'] = True
            ctx.obj['build_parents_count'] = int(count) if count else None  # Default to 1 if no number is specified

        return click.Group.get_command(self, ctx, cmd_name)

    def list_commands(self, ctx):
        # List of all commands
        return ['build', 'trun', 'run', 'test', 'compile', 'clip-compile', 'unittest', 'sbuild', 'pbuild', 'build-docs', 'build-unit']


cdbt = CustomCmdLoader()


@cdbt.command()
@click.option('--full-refresh', '-f', is_flag=True, help='Run a full refresh on all models.')
@click.option('--select', '-s', type=str, help='DBT style select string')
@click.option('--fail-fast', is_flag=True, help='Fail fast on errors.')
@click.option('--threads', '-t', type=int, help='Number of threads to use during DBT operations.')
@click.pass_context
def build(ctx, full_refresh, select, fail_fast, threads):
    """Execute a DBT build command passthrough."""
    cdbt_class.build(ctx, full_refresh, select, fail_fast, threads)


@cdbt.command()
@click.option('--full-refresh', '-f', is_flag=True, help='Run a full refresh on all models.')
@click.option('--select', '-s', type=str, help='DBT style select string')
@click.option('--fail-fast', is_flag=True, help='Fail fast on errors.')
@click.option('--threads', '-t', type=int, help='Number of threads to use during DBT operations.')
@click.pass_context
def trun(ctx, full_refresh, select, fail_fast, threads):
    """Execute a DBT run, then test command."""
    cdbt_class.trun(ctx, full_refresh, select, fail_fast, threads)


@cdbt.command()
@click.option('--full-refresh', '-f', is_flag=True, help='Run a full refresh on all models.')
@click.option('--select', '-s', type=str, help='DBT style select string')
@click.option('--fail-fast', is_flag=True, help='Fail fast on errors.')
@click.option('--threads', '-t', type=int, help='Number of threads to use during DBT operations.')
@click.pass_context
def run(ctx, full_refresh, select, fail_fast, threads):
    """Pass through to DBT run command."""
    cdbt_class.run(ctx, full_refresh, select, fail_fast, threads)


@cdbt.command()
@click.option('--select', '-s', type=str, help='DBT style select string')
@click.option('--fail-fast', is_flag=True, help='Fail fast on errors.')
@click.option('--threads', '-t', type=int, help='Number of threads to use during DBT operations.')
@click.pass_context
def test(ctx, select, fail_fast, threads):
    """Pass through to DBT test command."""
    cdbt_class.test(ctx, select, fail_fast, threads)

@cdbt.command()
@click.option('--select', '-s', type=str, help='DBT style select string')
@click.option('--fail-fast', is_flag=True, help='Fail fast on errors.')
@click.pass_context
def unittest(ctx, select, fail_fast):
    """Run unit tests on models."""
    cdbt_class.unittest(ctx, select, fail_fast)

@cdbt.command()
@click.option('--select', '-s', type=str, help='Name of the model(s) to compile.')
@click.pass_context
def compile(ctx, select):
    """Pass through to DBT compile."""
    cdbt_class.compile(ctx, select)

@cdbt.command()
@click.option('--select', '-s', type=str, help='Name of the model to compile. Recommend only running one.')
@click.pass_context
def clip_compile(ctx, select):
    """Pass through to DBT compile."""
    cdbt_class.clip_compile(ctx, select)

@cdbt.command()
@click.option('--full-refresh', '-f', is_flag=True, help='Force a full refresh on all models in build scope.')
@click.option('--threads', '-t', type=int, help='Number of threads to use during DBT operations.')
@click.pass_context
def sbuild(ctx, full_refresh, threads):
    """Build models based on changes in current state since last build."""
    cdbt_class.sbuild(ctx, full_refresh, threads)


@cdbt.command()
@click.option('--full-refresh', '-f', is_flag=True, help='Force a full refresh on all models in build scope.')
@click.option('--threads', '-t', type=int, help='Number of threads to use during DBT operations.')
@click.pass_context
def pbuild(ctx, full_refresh, threads):
    """Build models based on changes from production to current branch."""
    cdbt_class.pbuild(ctx, full_refresh, threads)


@cdbt.command()
@click.pass_context
@click.option('--select', '-s', type=str, help='Name of the model to build unit test data for.')
def build_docs(ctx, select):
    """Build dbt YML model docs for a model"""
    dbt_docs = BuildDBTDocs()
    dbt_docs.main(select)


@cdbt.command()
@click.option('--select', '-s', type=str, help='Name of the model to build unit test data for.')
@click.pass_context
def build_unit(ctx, select):
    """Build unit test mock and expect data for a model."""
    build_unit_test_data = BuildUnitTestDataAI()
    build_unit_test_data.main(select)
