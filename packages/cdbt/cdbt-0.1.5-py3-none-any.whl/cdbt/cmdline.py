import click
import re

from cdbt.main import ColdBoreCapitalDBT

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
        return ['build', 'trun', 'run', 'test', 'compile', 'sbuild', 'pbuild']


cdbt = CustomCmdLoader()


@cdbt.command()
@click.option('--full-refresh', is_flag=True, help='Run a full refresh on all models.')
@click.option('--select', type=str, help='DBT style select string')
@click.option('--fail-fast', is_flag=True, help='Fail fast on errors.')
def build(full_refresh, select, fail_fast):
    cdbt_class.build(full_refresh, select, fail_fast)


@cdbt.command()
@click.option('--full-refresh', is_flag=True, help='Run a full refresh on all models.')
@click.option('--select', type=str, help='DBT style select string')
@click.option('--fail-fast', is_flag=True, help='Fail fast on errors.')
def trun(full_refresh, select, fail_fast):
    cdbt_class.trun(full_refresh, select, fail_fast)


@cdbt.command()
@click.option('--full-refresh', is_flag=True, help='Run a full refresh on all models.')
@click.option('--select', type=str, help='DBT style select string')
@click.option('--fail-fast', is_flag=True, help='Fail fast on errors.')
def run(full_refresh, select, fail_fast):
    cdbt_class.run(full_refresh, select, fail_fast)


@cdbt.command()
@click.option('--select', type=str, help='DBT style select string')
@click.option('--fail-fast', is_flag=True, help='Fail fast on errors.')
def test(select, fail_fast):
    cdbt_class.test(select, fail_fast)


@cdbt.command()
def compile():
    cdbt_class.compile()


@cdbt.command()
@click.option('--full-refresh', is_flag=True, help='Force a full refresh on all models in build scope.')
@click.pass_context
def sbuild(ctx, full_refresh):
    cdbt_class.sbuild(ctx, full_refresh)


@cdbt.command()
@click.option('--full-refresh', is_flag=True, help='Force a full refresh on all models in build scope.')
@click.pass_context
def pbuild(ctx, full_refresh):
    cdbt_class.pbuild(ctx, full_refresh)
