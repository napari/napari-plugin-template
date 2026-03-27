"""
test_create_template
--------------------
"""

import os
import subprocess
import sys
from pathlib import Path
from shutil import which

import pytest

LATEST_SUPPORTED_PYTHON = '3.14'

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

FEATURE_CASES = [
    {},
    {'include_reader_plugin': False},
    {'include_writer_plugin': False},
    {'include_sample_data_plugin': False},
    {'include_widget_plugin': False},
    {
        'include_reader_plugin': False,
        'include_writer_plugin': False,
        'include_sample_data_plugin': False,
        'include_widget_plugin': False,
    },
]


def build_answers(**overrides):
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

    pyproject_text = result.project_dir.joinpath('pyproject.toml').read_text(
        encoding='utf-8'
    )
    assert f'Programming Language :: Python :: {LATEST_SUPPORTED_PYTHON}' in pyproject_text
    assert '[tool.pixi.workspace]' in pyproject_text
    assert '[tool.pixi.tasks]' in pyproject_text
    assert not result.project_dir.joinpath('tox.ini').exists()


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


def run_generated_tests(plugin_directory):
    """Run the generated project's test suite via pixi."""
    if which('pixi') is None:
        pytest.fail(
            'pixi must be available in PATH to run generated smoke tests'
        )

    project_dir = Path(plugin_directory)
    env = os.environ.copy()
    env.pop('PIXI_PROJECT_MANIFEST', None)
    env.pop('PIXI_IN_SHELL', None)
    try:
        subprocess.run(
            ['pixi', 'run', 'test'],
            cwd=project_dir,
            check=True,
            capture_output=True,
            text=True,
            env=env,
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
    """Run a couple of generated projects end to end via pixi."""
    answers = build_answers()
    result = copie.copy(extra_answers=answers)

    assert_generated_layout(
        result, answers['plugin_name'], answers['module_name']
    )
    assert_feature_files(result, answers)
    run_generated_tests(result.project_dir)


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

    Pre-commit validity doesn't vary with the plugin-type combination flags —
    what matters is that the generated files are lint-clean.  Running all 16
    parametrize combinations takes significant CI time for no additional
    coverage, so we test the richest case (all contribution types enabled).
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
            [sys.executable, '-m', 'pre_commit', 'run', '--all-files', '--show-diff-on-failure'],
            cwd=str(result.project_dir),
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as error:
        pytest.fail(
            f'pre-commit failed with output:\n{error.stdout.decode()}\n'
            f'error:\n{error.stderr.decode()}'
        )
