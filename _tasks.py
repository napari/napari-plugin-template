import contextlib
import os
import re
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path


# ANSI color codes for better visual output
class Colors:
    """ANSI color codes for terminal output."""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @staticmethod
    def success(msg):
        return f"{Colors.GREEN}✔ {msg}{Colors.END}"

    @staticmethod
    def info(msg):
        return f"{Colors.BLUE}ℹ {msg}{Colors.END}"

    @staticmethod
    def warning(msg):
        return f"{Colors.YELLOW}⚠ {msg}{Colors.END}"

    @staticmethod
    def error(msg):
        return f"{Colors.RED}✗ {msg}{Colors.END}"

    @staticmethod
    def step(num, total, msg):
        return f"{Colors.BOLD}[{num}/{total}]{Colors.END} {msg}"


def module_name_pep8_compliance(module_name):
    """Validate that the plugin module name is PEP8 compliant."""
    if not re.match(r'^[a-z][_a-z0-9]+$', module_name):
        link = 'https://www.python.org/dev/peps/pep-0008/#package-and-module-names'
        print(Colors.error('Module name should be PEP-8 compliant.'))
        print(f'  More info: {link}')
        sys.exit(1)


def pypi_package_name_compliance(plugin_name):
    """Check there are no underscores in the plugin name"""
    if re.search(r'_', plugin_name):
        print(Colors.error('PyPI.org and pip discourage package names with underscores.'))
        sys.exit(1)


def validate_manifest(module_name, project_directory):
    """Validate the new plugin repository against napari requirements."""
    try:
        from npe2 import PluginManifest
    except ImportError:
        print(Colors.warning('npe2 is not installed. Skipping manifest validation.'))
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
        msg = f"Manifest for '{pm.display_name or pm.name}' is valid!"
        valid = True
    except PluginManifest.ValidationError as err:
        print(Colors.error(f'Invalid manifest: {err}'))
        sys.exit(1)
    except (FileNotFoundError, PermissionError, OSError) as err:
        print(Colors.error(f'Failed to read {path!r}. {type(err).__name__}: {err}'))
        sys.exit(1)
    else:
        print(Colors.success(msg))
        return valid


def initialize_new_repository(
    install_precommit=False,
    plugin_name='napari-foobar',
    plugin_directory='napari-foobar',
    github_repository_url='provide later',
    github_username_or_organization='githubuser',
):
    """Initialize new plugin repository with git, and optionally pre-commit."""

    print("\n" + "="*50)
    print(Colors.info("Setting up your plugin repository..."))
    print("="*50 + "\n")

    # Configure git to suppress line ending warnings
    git_env = os.environ.copy()
    git_env['GIT_CONFIG_GLOBAL'] = os.devnull  # Prevent reading global config

    # Configure git line ending settings quietly
    # devnull to suppress output
    if os.name == 'nt':  # if on Windows, configure git line ending characters
        subprocess.run(
            ['git', 'config', '--global', 'core.autocrlf', 'true'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:  # for Linux and Mac
        subprocess.run(
            ['git', 'config', '--global', 'core.autocrlf', 'input'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    # Initialize git repository
    try:
        print(Colors.info("Initializing git repository..."))
        subprocess.run(
            ['git', 'init', '-q'],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ['git', 'checkout', '-b', 'main'],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(Colors.success("Git repository initialized"))
    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
        print(Colors.error(f'Error in git initialization: {e}'))
        return _generate_manual_setup_message(plugin_name, plugin_directory, github_repository_url, github_username_or_organization)

    if install_precommit is True:
        print(Colors.info("Setting up pre-commit hooks..."))
        # Try to install and update pre-commit
        try:
            # Check if we're in a uv environment to use uv's pip if available
            in_uv_env = 'UV_PROJECT_ENVIRONMENT' in os.environ or subprocess.run(
                ['uv', '--version'],
                capture_output=True,
                text=True
            ).returncode == 0

            if in_uv_env:
                # Use uv to install pre-commit
                subprocess.run(
                    ['uv', 'pip', 'install', 'pre-commit'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True,
                )
            else:
                # Use regular pip
                subprocess.run(
                    ['python', '-m', 'pip', 'install', 'pre-commit'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True,
                )

            # Update pre-commit hooks
            subprocess.run(
                ['pre-commit', 'autoupdate'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            # Stage files and run pre-commit formatting
            subprocess.run(
                ['git', 'add', '.'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
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
            print(Colors.success("Pre-commit hooks configured"))
        except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
            print(Colors.warning(f'Could not install pre-commit (this is optional): {e}'))

    # Create initial commit
    try:
        print(Colors.info("Creating initial commit..."))
        subprocess.run(['git', 'add', '.'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(
            ['git', 'commit', '-q', '-m', 'initial commit'],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(Colors.success("Initial commit created"))
    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
        print(Colors.error(f'Error creating initial git commit: {e}'))
        return _generate_manual_setup_message(plugin_name, plugin_directory, github_repository_url, github_username_or_organization)

    # Ensure full read/write/execute permissions for .git files on Windows
    if os.name == 'nt':
        with contextlib.suppress(Exception):
            subprocess.run(
                ['attrib', '-h', '-r', '.git', '/s', '/d'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    # Install pre-commit hooks after initial commit
    if install_precommit is True:
        try:
            subprocess.run(
                ['pre-commit', 'install'],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(Colors.success("Pre-commit hooks installed"))
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            print(Colors.warning('Could not install pre-commit hooks (this is optional)'))

    return _generate_next_steps_message(plugin_name, plugin_directory, github_repository_url, github_username_or_organization)


def _generate_manual_setup_message(plugin_name, plugin_directory, github_repository_url, github_username_or_organization):
    """Generate message for manual setup when git initialization fails."""
    msg = f"""
{Colors.warning('Git initialization had issues. Please set up manually:')}

{Colors.step(1, 4, 'Navigate to your plugin directory:')}
    cd {plugin_directory}

{Colors.step(2, 4, 'Initialize git repository:')}
    git init -b main
    git add .
    git commit -m 'initial commit'

{Colors.step(3, 4, 'Install your plugin in development mode:')}
    pip install -e .[all]
{Colors.info('This installs your plugin with napari and default Qt bindings in editable mode.')}

{Colors.step(4, 4, 'Create and link GitHub repository:')}"""

    if github_repository_url != 'provide later':
        msg += f"""
    Create at: https://github.com/{github_username_or_organization}/{plugin_name}
    Then run:
        git remote add origin https://github.com/{github_username_or_organization}/{plugin_name}.git
        git push -u origin main"""
    else:
        msg += """
    Create at: https://github.com/new
    Then link it to your local repository."""

    return msg


def _generate_next_steps_message(plugin_name, plugin_directory, github_repository_url, github_username_or_organization):
    """Generate the next steps message after successful initialization."""

    msg = f"""
{"="*50}
{Colors.BOLD}{Colors.GREEN}✔ Your plugin template is ready!{Colors.END}
{"="*50}
{Colors.step(1, 5, 'Install your plugin in development mode:')}
    cd {plugin_directory}
    pip install -e .[all]

{Colors.info('This installs your plugin with napari and default Qt bindings in editable mode.')}
"""

    if github_repository_url != 'provide later':
        msg += f"""
{Colors.step(2, 5, f"Create a GitHub repository named '{plugin_name}':")}
    https://github.com/{github_username_or_organization}/{plugin_name}

{Colors.step(3, 5, 'Link and push to GitHub:')}
    git remote add origin https://github.com/{github_username_or_organization}/{plugin_name}.git
    git push -u origin main

{Colors.step(4, 5, 'Review your project URLs in pyproject.toml:')}
    The following URLs will appear on the napari hub:
    • Bug Tracker: https://github.com/{github_username_or_organization}/{plugin_name}/issues
    • Documentation: https://github.com/{github_username_or_organization}/{plugin_name}#README.md
    • Source Code: https://github.com/{github_username_or_organization}/{plugin_name}
    • User Support: https://github.com/{github_username_or_organization}/{plugin_name}/issues
"""
    else:
        msg += f"""
{Colors.step(2, 5, 'Create a GitHub repository:')}
    https://github.com/new

{Colors.step(3, 5, 'Link and push to GitHub:')}
    git remote add origin https://github.com/YOUR-USERNAME/{plugin_name}.git
    git push -u origin main

{Colors.step(4, 5, 'Add project URLs to pyproject.toml:')}
    Consider adding these URLs under the project_urls key:
        [project.urls]
        Bug Tracker = https://github.com/your-repo-username/your-repo-name/issues
        Documentation = https://github.com/your-repo-username/your-repo-name#README.md
        Source Code = https://github.com/your-repo-username/your-repo-name
        User Support = https://github.com/your-repo-username/your-repo-name/issues
"""

    msg += f"""
{Colors.step(5, 5, 'Customize your plugin:')}
    • Optionally edit .napari-hub/DESCRIPTION.md for your napari hub listing
    • Customize metadata: https://github.com/chanzuckerberg/napari-hub/blob/main/docs/customizing-plugin-listing.md
    • Read the the plugin guide: https://napari.org/stable/plugins/building_a_plugin/index.html

{"="*50}
{Colors.success('Happy plugin development! 🚀')}
{"="*50}
"""
    return msg


if __name__ == '__main__':
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
