import click
from .gptvision import gptvision
from .geminivision import geminivision
from .copyprompt import copyprompt
from .solution import solution
from .gptloop import gptloop
from . import __version__

CONTEXT_SETTINGS = dict(
    help_option_names=[
        '-h',
        '--help'
    ],
    auto_envvar_prefix='VBIMAGETOTEXT',
)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__, prog_name='vbimagetotext')
def main():
    pass


main.add_command(gptvision)
main.add_command(geminivision)
main.add_command(copyprompt)
main.add_command(solution)
main.add_command(gptloop)
