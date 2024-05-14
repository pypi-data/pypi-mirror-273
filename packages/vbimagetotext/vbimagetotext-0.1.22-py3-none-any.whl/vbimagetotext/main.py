import click
from .gptvision import gptvision
from .geminivision import geminivision
from .copyprompt import copyprompt
from .solution import solution
from .gptloop import gptloop
import os
import toml


def get_version():
    # Get the directory that this script file is located in
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to the pyproject.toml file
    pyproject_path = os.path.join(script_dir, 'pyproject.toml')

    # Load the pyproject.toml file
    pyproject = toml.load(pyproject_path)

    return pyproject['tool']['poetry']['version']


__version__ = get_version()


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
