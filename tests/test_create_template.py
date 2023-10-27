"""
test_create_template
--------------------
"""


import os
import subprocess

import pytest


def run_tox(plugin):
    """Run the tox suite of the newly created plugin."""
    try:
        subprocess.check_call(
            ["tox", "-c", os.path.join(plugin, "tox.ini"), "-e", "py", "--", plugin]
        )
    except subprocess.CalledProcessError as e:
        pytest.fail("Subprocess fail", pytrace=True)


def test_run_cookiecutter_and_plugin_tests(copie, capsys):
    """Create a new plugin via cookiecutter and run its tests."""
    result = copie.copy(extra_answers={"plugin_name": "foo-bar"})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir.name == "foo-bar"
    assert result.project_dir.is_dir()
    assert result.project_dir.joinpath("src").is_dir()
    assert result.project_dir.joinpath("src", "foo_bar", "__init__.py").is_file()
    assert result.project_dir.joinpath("src", "foo_bar", "_tests", "test_reader.py").is_file()

    run_tox(str(result.project_dir))


def test_run_cookiecutter_and_plugin_tests_with_napari_prefix(copie, capsys):
    """make sure it's also ok to use napari prefix."""
    result = copie.copy(extra_answers={"plugin_name": "napari-foo"})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir.name == "napari-foo"
    assert result.project_dir.is_dir()
    assert result.project_dir.joinpath("src").is_dir()
    assert result.project_dir.joinpath("src", "napari_foo", "__init__.py").is_file()
    assert result.project_dir.joinpath("src", "napari_foo", "_tests", "test_reader.py").is_file()


def test_run_cookiecutter_select_plugins(copie, capsys):
    """make sure it's also ok to use napari prefix."""
    result = copie.copy(
        extra_answers={
            "plugin_name": "anything",
            "include_widget_plugin": "n",
            "include_writer_plugin": "n",
        }
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir.name == "anything"
    assert result.project_dir.is_dir()
    assert result.project_dir.joinpath("src").is_dir()
    assert result.project_dir.joinpath("src", "anything", "__init__.py").is_file()
    assert result.project_dir.joinpath("src", "anything", "_tests", "test_reader.py").is_file()

    assert not result.project_dir.joinpath("src", "anything", "_widget.py").is_file()
    assert not result.project_dir.joinpath(
        "src", "anything", "_tests", "test_widget.py"
    ).is_file()
    assert not result.project_dir.joinpath("src", "anything", "_writer.py").is_file()
    assert not result.project_dir.joinpath(
        "src", "anything", "_tests", "test_writer.py"
    ).is_file()


@pytest.mark.parametrize("include_reader_plugin", [True, False])
@pytest.mark.parametrize("include_writer_plugin", [True, False])
@pytest.mark.parametrize("include_sample_data_plugin", [True, False])
@pytest.mark.parametrize("include_widget_plugin", [True, False])
def test_pre_commit_validity(copie, include_reader_plugin, include_writer_plugin, include_sample_data_plugin, include_widget_plugin):
    result = copie.copy(
        extra_answers={
            "plugin_name": "anything",
            "include_reader_plugin": include_reader_plugin,
            "include_writer_plugin": include_writer_plugin,
            "include_sample_data_plugin": include_sample_data_plugin,
            "include_widget_plugin": include_widget_plugin,
            "install_precommit": True,
        }
    )
    result.project_dir.joinpath("setup.cfg").is_file()
    try:
        subprocess.run(["pre-commit", "run", "--all", "--show-diff-on-failure"], cwd=str(result.project_dir), check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"pre-commit failed with output:\n{e.stdout.decode()}\nerrror:\n{e.stderr.decode()}")
