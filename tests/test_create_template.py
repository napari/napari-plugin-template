"""
test_create_template
--------------------
Validates that the copier template renders correctly and that generated
projects are functional.

Test strategy
~~~~~~~~~~~~~
- ``test_rendered_feature_matrix``: Quickly renders a representative set of
  feature combinations and checks file layout / ``pyproject.toml`` content.
  This is the broad coverage layer — many cases, no subprocesses.
- ``test_generated_project_smoke_tests``: Renders the fully-featured template
  (all plugins enabled) and runs its test suite via tox end to end.
- ``test_run_plugin_tests_with_napari_prefix``: Exercises the ``napari-``
  naming path (module-name inference, directory layout).
- ``test_run_select_plugins`` / ``test_pre_commit_validity``: Targeted checks
  for copier boolean-prompt handling and pre-commit hook validity.

Running
~~~~~~~
These tests are best executed via ``tox`` (not plain ``pytest``) so that
``pytest-copie`` and ``tox-uv`` are present in the test environment::

    tox                               # all envs
    tox -e py313                      # single interpreter
    tox -e py313 -- tests/test_create_template.py::test_pre_commit_validity
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Shared fixture data
# ---------------------------------------------------------------------------

# Base answers applied to every generated project.  Feature flags
# (include_*_plugin) are intentionally absent here so that copier uses its
# template defaults (all True).  Override individual flags via build_answers()
# to test the disabled paths without repeating all of the boilerplate.
DEFAULT_ANSWERS = {
    'plugin_name': 'foo-bar',
    'display_name': 'Foo Bar',
    'module_name': 'foo_bar',
    'short_description': 'Super fast foo for all the bars',
    'full_name': 'napari bot',
    'email': 'etal@example.com',
    'github_username_or_organization': 'napari',
    'install_precommit': False,
}

# Representative feature-flag combinations for the parametrized render test.
# Rather than exhaustively testing all 2**4 = 16 combinations (slow and
# largely redundant for render-only checks), we cover:
#   • all features enabled   (default path)
#   • each feature disabled individually   (ensures each conditional works)
#   • all features disabled simultaneously (ensures nothing breaks when empty)
FEATURE_CASES = [
    {},                                          # all features enabled (default)
    {'include_reader_plugin': False},            # reader absent
    {'include_writer_plugin': False},            # writer absent
    {'include_sample_data_plugin': False},       # sample-data absent
    {'include_widget_plugin': False},            # widget absent
    {                                            # all features disabled
        'include_reader_plugin': False,
        'include_writer_plugin': False,
        'include_sample_data_plugin': False,
        'include_widget_plugin': False,
    },
]


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def build_answers(**overrides):
    """Return a copy of DEFAULT_ANSWERS with keyword overrides applied."""
    answers = DEFAULT_ANSWERS.copy()
    answers.update(overrides)
    return answers


def assert_generated_layout(result, plugin_name, module_name):
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir.is_dir()
    assert result.project_dir.joinpath('src').is_dir()
    assert result.project_dir.joinpath(
        'src', module_name, '__init__.py'
    ).is_file()
    with open(result.project_dir / 'README.md', encoding='utf-8') as handle:
        assert handle.readline() == f'# {plugin_name}\n'


def assert_feature_files(result, answers):
    test_path = result.project_dir.joinpath('tests')
    pyproject_text = result.project_dir.joinpath('pyproject.toml').read_text(
        encoding='utf-8'
    )
    expected = {
        'test_reader.py': answers.get('include_reader_plugin', True),
        'test_writer.py': answers.get('include_writer_plugin', True),
        'test_sample_data.py': answers.get('include_sample_data_plugin', True),
        'test_widget.py': answers.get('include_widget_plugin', True),
    }

    for file_name, is_expected in expected.items():
        assert test_path.joinpath(file_name).is_file() is is_expected

    if answers.get('include_widget_plugin', True):
        assert '    "magicgui",' in pyproject_text
        assert '    "pytest-qt",' in pyproject_text
        assert '    "napari[qt]",' in pyproject_text
    else:
        assert '    "magicgui",' not in pyproject_text
        assert '    "pytest-qt",' not in pyproject_text
        assert '    "napari[qt]",' not in pyproject_text


def _generated_project_env():
    """Return an environment suitable for running commands inside generated projects.

    Strips ``TOX_*`` variables so that the generated project's tox invocation
    does not inherit settings (e.g. ``TOX_ENV_NAME``, ``TOX_WORK_DIR``) from
    the outer tox process running *these* tests.  Also strips ``VIRTUAL_ENV``
    to prevent pip/uv from accidentally targeting our test virtualenv instead
    of creating a fresh one for the generated project.
    """
    env = os.environ.copy()
    for key in tuple(env):
        if key.startswith('TOX_'):
            env.pop(key)
    env.pop('VIRTUAL_ENV', None)
    return env


def _current_tox_env():
    """Return the tox environment name matching the currently-running interpreter.

    The generated template's ``tox.ini`` defines environments using the scheme
    ``py3{10,11,12,13}-{linux,macos,windows}``, so we must select the exact
    matching env when invoking tox on the generated project.  Example output
    on CPython 3.13 / Windows: ``py313-windows``.
    """
    platform = 'linux'
    if sys.platform == 'darwin':
        platform = 'macos'
    elif sys.platform.startswith('win'):
        platform = 'windows'
    return f'py{sys.version_info.major}{sys.version_info.minor}-{platform}'


def run_generated_tests(plugin_directory):
    """Run the generated project's test suite via tox with tox-uv enabled.

    Uses the plain ``tox`` executable  because our own test environment
    already has tox and tox-uv installed.  The ``tox-uv`` plugin is
    therefore active and the generated project's dependencies are resolved
    through uv, matching the way the template's own CI works.
    """
    with tempfile.TemporaryDirectory(prefix='npt-tox-') as tox_workdir:
        try:
            subprocess.run(
                [
                    'tox',
                    '-c',
                    os.path.join(plugin_directory, 'tox.ini'),
                    '--workdir',
                    tox_workdir,
                    '-e',
                    _current_tox_env(),
                ],
                cwd=Path(plugin_directory),
                check=True,
                capture_output=True,
                text=True,
                env=_generated_project_env(),
                timeout=600,
            )
        except subprocess.CalledProcessError as error:
            pytest.fail(
                'Generated project smoke test failed:\n'
                f'stdout:\n{error.stdout}\n'
                f'stderr:\n{error.stderr}'
            )


@pytest.mark.parametrize('overrides', FEATURE_CASES)
def test_rendered_feature_matrix(copie, overrides):
    """Render representative feature combinations quickly."""
    answers = build_answers(**overrides)
    result = copie.copy(extra_answers=answers)

    assert_generated_layout(
        result, answers['plugin_name'], answers['module_name']
    )
    assert_feature_files(result, answers)


def test_generated_project_smoke_tests(copie):
    """Run one fully-featured generated project end to end via tox.

    Uses the default (all-features) answers so the smoke test exercises the
    widest possible code path: readers, writers, sample data, *and* widgets.
    This is intentionally the slow test in the suite (~60s on a warm uv
    cache) and serves as the primary integration gate for the template.
    """
    answers = build_answers()  # all features enabled
    result = copie.copy(extra_answers=answers)

    assert_generated_layout(
        result, answers['plugin_name'], answers['module_name']
    )
    assert_feature_files(result, answers)
    run_generated_tests(str(result.project_dir))


def test_run_plugin_tests_with_napari_prefix(copie):
    """Make sure it is also ok to use the napari prefix."""
    name = 'napari-foo'
    result = copie.copy(
        extra_answers=build_answers(
            plugin_name=name,
            display_name='napari Foo',
            module_name='napari_foo',
        )
    )

    assert_generated_layout(result, name, 'napari_foo')
    assert result.project_dir.joinpath('tests', 'test_reader.py').is_file()


def test_run_select_plugins(copie):
    """Make sure boolean prompts behave with copier's short answers."""
    name = 'anything'
    result = copie.copy(
        extra_answers=build_answers(
            plugin_name=name,
            module_name=name,
            include_widget_plugin='n',
            include_writer_plugin='n',
        )
    )

    assert_generated_layout(result, name, name)
    assert result.project_dir.joinpath('tests', 'test_reader.py').is_file()
    assert not result.project_dir.joinpath('src', name, '_widget.py').is_file()
    assert not result.project_dir.joinpath('tests', 'test_widget.py').is_file()
    assert not result.project_dir.joinpath('src', name, '_writer.py').is_file()
    assert not result.project_dir.joinpath('tests', 'test_writer.py').is_file()


def test_pre_commit_validity(copie):
    """Verify pre-commit passes on a fully-featured generated plugin.

    Pre-commit validity doesn't vary with the plugin-type combination flags.
    Run the richest case once instead of every feature combination.
    """
    result = copie.copy(
        extra_answers=build_answers(
            plugin_name='anything',
            display_name='Foo Bar',
            module_name='anything',
            include_reader_plugin=True,
            include_writer_plugin=True,
            include_sample_data_plugin=True,
            include_widget_plugin=True,
            install_precommit=True,
        )
    )
    assert result.exit_code == 0
    assert result.project_dir.joinpath('pyproject.toml').is_file()
    try:
        subprocess.run(
            [
                sys.executable,
                '-m',
                'pre_commit',
                'run',
                '--all-files',
                '--show-diff-on-failure',
            ],
            cwd=str(result.project_dir),
            check=True,
            capture_output=True,
            env=_generated_project_env(),
        )
    except subprocess.CalledProcessError as error:
        pytest.fail(
            f'pre-commit failed with output:\n{error.stdout.decode()}\n'
            f'error:\n{error.stderr.decode()}'
        )
