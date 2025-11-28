import logging
import os
import re
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path


def module_name_pep8_compliance(module_name):
    """Validate that the plugin module name is PEP8 compliant."""
    if not re.match(r'^[a-z][_a-z0-9]+$', module_name):
        link = 'https://www.python.org/dev/peps/pep-0008/#package-and-module-names'
        logger.error('Module name should be pep-8 compliant.')
        logger.error('  More info: %s', link)
        sys.exit(1)


def pypi_package_name_compliance(plugin_name):
    """Check there are no underscores in the plugin name"""
    if re.search(r'_', plugin_name):
        logger.error(
            'PyPI.org and pip discourage package names with underscores.'
        )
        sys.exit(1)


def validate_manifest(module_name, project_directory):
    """Validate the new plugin repository against napari requirements."""
    try:
        from npe2 import PluginManifest
    except ImportError:
        logger.error('npe2 is not installed. Skipping manifest validation.')
        return True

    current_directory = Path('.').absolute()
    if (
        current_directory.match(project_directory)
        and not Path(project_directory).is_absolute()
    ):
        project_directory = current_directory

    path = Path(project_directory) / 'src' / Path(module_name) / 'napari.yaml'

    valid = False
    try:
        pm = PluginManifest.from_file(path)
        msg = f'✔ Manifest for {(pm.display_name or pm.name)!r} valid!'
        valid = True
    except PluginManifest.ValidationError as err:
        msg = f'🅇 Invalid! {err}'
        logger.error(msg.encode('utf-8'))
        sys.exit(1)
    except (FileNotFoundError, PermissionError, OSError) as err:
        msg = f'🅇 Failed to read {path!r}. {type(err).__name__}: {err}'
        logger.error(msg.encode('utf-8'))
        sys.exit(1)
    else:
        logger.info(msg.encode('utf-8'))
        return valid


def initialize_new_repository(
    install_precommit=False,
    plugin_name='napari-foobar',
    plugin_directory='napari-foobar',
    github_repository_url='provide later',
    github_username_or_organization='githubuser',
):
    """Initialize new plugin repository with git, and optionally pre-commit."""

    msg = ''

    # Configure git line ending settings
    # https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration
    if os.name == 'nt':  # if on Windows, configure git line ending characters
        subprocess.run(['git', 'config', '--global', 'core.autocrlf', 'true'])
    else:  # for Linux and Mac
        subprocess.run(['git', 'config', '--global', 'core.autocrlf', 'input'])

    # try to run git init
    try:
        subprocess.run(['git', 'init', '-q'], check=True)
        subprocess.run(['git', 'checkout', '-b', 'main'], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        logger.error('Error in git initialization.')

    if install_precommit is True:
        # try to install and update pre-commit
        try:
            print('install pre-commit ...')
            subprocess.run(
                ['python', '-m', 'pip', 'install', 'pre-commit'],
                stdout=subprocess.DEVNULL,
            )
            print('updating pre-commit...')
            subprocess.run(
                ['pre-commit', 'autoupdate'], stdout=subprocess.DEVNULL
            )
            subprocess.run(['git', 'add', '.'])
            # Run both ruff hooks to match template pre-commit config
            subprocess.run(
                ['pre-commit', 'run', 'ruff-check', '-a'],
                capture_output=True,
                check=False,
            )
            subprocess.run(
                ['pre-commit', 'run', 'ruff-format', '-a'],
                capture_output=True,
                check=False,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            logger.error('Error pip installing then running pre-commit.')

    try:
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(
            ['git', 'commit', '-q', '-m', 'initial commit'], check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        logger.error('Error creating initial git commit.')
        msg += f"""
Your plugin template is ready!  Next steps:
1. `cd` into your new directory and initialize a git repo
(this is also important for version control!)
    cd {plugin_directory}
    git init -b main
    git add .
    git commit -m 'initial commit'
    # you probably want to install your new package into your environment
    # the below command will install the package in editable mode with
    # napari and Qt bindings
    pip install -e .[all]
"""
    else:
        msg += f"""
Your plugin template is ready!  Next steps:
1. `cd` into your new directory
    cd {plugin_directory}
    # Use the following command to install your package in editable mode,
    # as well as napari and Qt bindings into your existing environment.
    pip install -e .[all]
"""
    # Ensure full reqd/write/execute permissions for .git files
    if os.name == 'nt':  # if on Windows OS
        # Avoid permission denied errors on Github Actions CI
        subprocess.run(['attrib', '-h', 'rr', '.git', '/s', '/d'])

    if install_precommit is True:
        # try to install and update pre-commit
        # installing after commit to avoid problem with comments in pyproject.toml.
        try:
            print('install pre-commit hook...')
            subprocess.run(['pre-commit', 'install'], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            logger.error('Error at pre-commit install, skipping pre-commit')

    if github_repository_url != 'provide later':
        msg += f"""
    2. Create a github repository with the name '{plugin_name}':
    https://github.com/{github_username_or_organization}/{plugin_name}.git
    3. Add your newly created github repo as a remote and push:
        git remote add origin https://github.com/{github_username_or_organization}/{plugin_name}.git
        git push -u origin main
    4. The following default URLs have been added to `pyproject.toml`:
        Bug Tracker = https://github.com/{github_username_or_organization}/{plugin_name}/issues
        Documentation = https://github.com/{github_username_or_organization}/{plugin_name}#README.md
        Source Code = https://github.com/{github_username_or_organization}/{plugin_name}
        User Support = https://github.com/{github_username_or_organization}/{plugin_name}/issues
        These URLs will be displayed on your plugin's napari hub page.
        You may wish to change these before publishing your plugin!"""
    else:
        msg += """
    2. Create a github repository for your plugin:
    https://github.com/new
    3. Add your newly created github repo as a remote and push:
        git remote add origin https://github.com/your-repo-username/your-repo-name.git
        git push -u origin main
    4. Consider adding additional links for documentation and user support to pyproject.toml
    using the project_urls key e.g.
        [project.urls]
        Bug Tracker = https://github.com/your-repo-username/your-repo-name/issues
        Documentation = https://github.com/your-repo-username/your-repo-name#README.md
        Source Code = https://github.com/your-repo-username/your-repo-name
        User Support = https://github.com/your-repo-username/your-repo-name/issues"""

    msg += """
    5. Read the README for more info: https://github.com/napari/napari-plugin-template
    6. We've provided a template description for your plugin page on the napari hub at `.napari-hub/DESCRIPTION.md`.
    You'll likely want to edit this before you publish your plugin.
    7. Consider customizing the rest of your plugin metadata for display on the napari hub:
    https://github.com/chanzuckerberg/napari-hub/blob/main/docs/customizing-plugin-listing.md
    """
    return msg


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('pre_gen_project')
    parser = ArgumentParser()
    parser.add_argument(
        '--plugin_name', dest='plugin_name', help='The name of your plugin'
    )
    parser.add_argument(
        '--module_name', dest='module_name', help='Plugin module name'
    )
    parser.add_argument(
        '--project_directory',
        dest='project_directory',
        help='Project directory',
    )
    parser.add_argument(
        '--install_precommit',
        dest='install_precommit',
        help='Install pre-commit',
        default='False',
    )
    parser.add_argument(
        '--github_repository_url',
        dest='github_repository_url',
        help='Github repository URL',
        default='provide later',
    )
    parser.add_argument(
        '--github_username_or_organization',
        dest='github_username_or_organization',
        help='Github user or organisation name',
        default='githubuser',
    )
    args = parser.parse_args()

    # Since bool("False") returns True, we need to check the actual string value
    if str(args.install_precommit).lower() == 'true':
        install_precommit = True
    else:
        install_precommit = False
    module_name_pep8_compliance(args.module_name)
    pypi_package_name_compliance(args.plugin_name)
    validate_manifest(args.module_name, args.project_directory)
    msg = initialize_new_repository(
        install_precommit=install_precommit,
        plugin_name=args.plugin_name,
        plugin_directory=args.project_directory,
        github_repository_url=args.github_repository_url,
        github_username_or_organization=args.github_username_or_organization,
    )
    print(msg)
