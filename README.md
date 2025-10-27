# napari-plugin-template

[![Test plugin template](https://github.com/napari/napari-plugin-template/actions/workflows/test.yml/badge.svg)](https://github.com/napari/napari-plugin-template/actions/workflows/test.yml)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/napari.svg)](https://python.org)  <!-- Use the versions supported by napari core -->
[![License](https://img.shields.io/pypi/l/napari.svg)](https://github.com/napari/napari-plugin-template/raw/main/LICENSE)
[![npe2](https://img.shields.io/badge/plugin-npe2-blue?link=https://napari.org/stable/plugins/index.html)](https://napari.org/stable/plugins/index.html)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)

**napari-plugin-template** is a convenient [copier](https://copier.readthedocs.io/en/stable/) template for authoring ([npe2](https://github.com/napari/npe2)-based) [napari](https://napari.org/) plugins.

Creating a plugin is a great way to extend napari's functionality. This repo provides a template to
simplify the development and distribution your plugin.

> [!TIP]
> If you are interested in creating a plugin, have any questions about the process, or simply want to show
off your progress, we encourage you to post on the [Zulip chat](napari.zulipchat.com), where the core team
and the napari community are always active and happy to give you feedback!
> You can also talk directly to some of the core team at the napari community meetings; check [here](https://napari.org/stable/community/meeting_schedule.html)
for the schedule to see which meeting time suits you. Don't worry if your plugin is not finished yet, the earlier you join, the better! We are there to help :)

---

> [!IMPORTANT]
> This repo is not meant to be cloned/forked directly! Instead, the copier application will be used to execute
the template and ask you for configuration information (or you may accept the template's sensible defaults).
> 
> Please read [Getting Started](#getting-started) below.

By default, copier will use the most recently tagged version of the `napari-plugin-template`;
to use the latest version in the main or development branch read the
[copier instructions](https://copier.readthedocs.io/en/stable/generating/#templates-versions)

## Features

Using the napari-plugin-template offers the following benefits:

- 🚀Installable [PyPI] package
- 🧪[tox] test suite, testing various python versions and platforms.
- 🗒️`README.md` file that contains useful information about your plugin
- ⚙️Continuous integration configuration for [github actions] that handles testing
  and deployment of tagged releases
- 🔋git-tag-based version management with [setuptools_scm]
- 🪪Choose from several licenses, including [BSD-3], [MIT], [MPL v2.0], [Apache
  v2.0], [GNU GPL v3.0], or [GNU LGPL v3.0]

The napari-plugin-template can be [applied to pre-existing Python projects](https://copier.readthedocs.io/en/stable/faq/#can-copier-be-applied-over-a-preexisting-project);
consider using this template to add any of the above features, including plugin functionality, to your project.
Conflicts between your current project and the template will be recognized after the template is complete,
allowing you to choose what files to overwrite.

## Getting Started

These instructions will walk you through how to create a napari plugin. It uses an application called copier
to prompt you for configuration input and does the work of creating a functioning, distributable plugin from your
source code.
Both options install the [Copier](https://copier.readthedocs.io/en/stable/) application,
the [jinja2-time](https://pypi.org/project/jinja2-time/) extension,
and the napari plugin engine [npe2](https://github.com/napari/npe2) to help validate your new plugin is configured correctly.

### Step 1: Navigate to the parent directory of your plugin.

In your shell (i.e. CLI, command prompt, terminal, bash), navigate to the directory where your plugin should live
(or, if you are running the template on a previous plugin, does live) using `cd`.
You can navigate in your file explorer to the parent directory and copy the full path
if you are unfamiliar with managing file directories from the shell.

For example, if you want to create a new plugin inside your Documents folder,
you could enter into the command line the equivalent to:

```bash
cd C:/Users/<username>/Documents
```

### Step 2: Install and run copier with the napari-plugin template

In the below instructions, replace `<new-plugin-name>` with the name of the plugin;
copier will create (or re-use) the folder in the parent directory with this `<new-plugin-name>`.
For example if you want to create `napari-growth-cone-finder` replace
`<new-plugin-name>` with `napari-growth-cone-finder`.

#### [Option 2A]: Use uv for an up-to-date, no environment utilization of copier

[uv](https://docs.astral.sh/uv/) can reduce complexity since it will
automatically install and manage a version of Python;
[install uv](https://docs.astral.sh/uv/getting-started/installation/) if needed.

First, navigate to the source directory that you would like 

The following command is then all you need to get started:

```bash
uv tool run --with jinja2-time --with npe2 copier copy --trust https://github.com/napari/napari-plugin-template <new-plugin-name>
```

#### [Option 2B]: Use a conda or virtual environment to run the plugin template

Using `conda`:

```bash
conda create -y --name copier-env python=3.12 copier jinja2-time npe2
conda activate copier-env
```

Or using `venv` and `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install copier jinja2-time npe2
```

The next command will use copier to use the napari-plugin-template to generate a new napari plugin project:

```bash
copier copy --trust https://github.com/napari/napari-plugin-template <new-plugin-name>
```

### Step 3: Enter plugin configuration information.

Copier prompts you to enter information about your plugin. For more detailed information on each prompt see
the [prompts reference](./PROMPTS.md).

<details open>
<summary>Configuration prompts</summary>

```sh
copier copy --trust https://github.com/napari/napari-plugin-template napari-growth-cone-finder

Welcome to the napari plugin template!
This template will help you create a new napari plugin with all the necessary structure of a Python package. 

For more detailed information about each prompt, see:
https://github.com/napari/napari-plugin-template/blob/main/PROMPTS.md

🎤 The name of your plugin, used to name the package and repository
   napari-growth-cone-finder
🎤 Display name for your plugin in the napari GUI
   Growth Cone Finder
🎤 Plugin module name, usually the same as the name of the package, but lowercase and with underscores
   napari_growth_cone_finder
🎤 Short description of what your plugin does
   A simple plugin for napari
🎤 Email address
   creator@example.com
🎤 Developer name
   Ramon y Cajal
🎤 Github user or organisation name
   creator
🎤 Github repository URL
   https://github.com/creator/napari-growth-cone-finder
🎤 Include reader plugin?
   Yes
🎤 Include writer plugin?
   Yes
🎤 Include sample data plugin?
   Yes
🎤 Include widget plugin?
   Yes
🎤 Install pre-commit? (Code formatting checks)
   Yes
🎤 Install dependabot? (Automatic security updates of dependency versions)
   Yes
🎤 Which licence do you want your plugin code to have?
   BSD-3

Select license:
1 - BSD-3
2 - MIT
3 - Mozilla Public License 2.0
4 - Apache Software License 2.0
5 - GNU LGPL v3.0
6 - GNU GPL v3.0
Choose from 1, 2, 3, 4, 5, 6 (1, 2, 3, 4, 5, 6) [1]: 1
```

</details>

After entering the configuration information, the following output will be displayed:

<details open>
<summary>Output</summary>

```sh
Copying from template version 0.0.0.post126.dev0+95d5ece
    create  .napari-hub
    create  .napari-hub/DESCRIPTION.md
    create  .napari-hub/config-yml
    create  .pre-commit-config.yaml
    create  README.md
    create  MANIFEST.in
    create  LICENSE
    create  .gitignore
    create  .github
    create  .github/workflows
    create  .github/workflows/test_and_deploy
    create  .github/dependabot.yml
    create  tox.ini
    create  pyproject.toml
    create  src
    create  src/napari_growth_cone_finder
    create  src/napari_growth_cone_finder/_writer.py
    create  src/napari_growth_cone_finder/_tests
    create  src/napari_growth_cone_finder/_tests/test_sample_data.py
    create  src/napari_growth_cone_finder/_tests/test_writer.py
    create  src/napari_growth_cone_finder/_tests/__init__.py
    create  src/napari_growth_cone_finder/_tests/test_widget.py
    create  src/napari_growth_cone_finder/_tests/test_reader.py
    create  src/napari_growth_cone_finder/_sample_data.py
    create  src/napari_growth_cone_finder/napari.yaml
    create  src/napari_growth_cone_finder/__init__.py
    create  src/napari_growth_cone_finder/_reader.py
    create  src/napari_growth_cone_finder/_widget.py

 > Running task 1 of 1: ['/Users/creator/Code/repos-napari/.venv/bin/python3', '/private/var/folders/hg/l3v3xynd45sbvd141f3rqh600000gn/T/copier.vcs.clone.i5ou6e_q/_tasks.py', '--plugin_name=napari-growth-cone-finder', '--module_name=napari_growth_cone_finder', '--project_directory=napari-growth-cone-finder', '--install_precommit=True', '--github_repository_url=https://github.com/creator/napari-growth-cone-finder', '--github_username_or_organization=creator']
INFO:pre_gen_project:b"\xe2\x9c\x94 Manifest for 'Growth Cone Finder' valid!"
Switched to a new branch 'main'
install pre-commit ...
/Users/creator/Code/repos-napari/.venv/bin/python: No module named pip
updating pre-commit...
install pre-commit hook...
pre-commit installed at .git/hooks/pre-commit

Your plugin template is ready!  Next steps:
1. `cd` into your new directory
    cd napari-growth-cone-finder
    # Use the following command to install your package in editable mode,
    # as well as napari and Qt bindings into your existing environment.
    pip install -e .[all]

    2. Create a github repository with the name 'napari-growth-cone-finder':
    https://github.com/creator/napari-growth-cone-finder.git
    3. Add your newly created github repo as a remote and push:
        git remote add origin https://github.com/creator/napari-growth-cone-finder.git
        git push -u origin main
    4. The following default URLs have been added to `pyproject.toml`:
        Bug Tracker = https://github.com/creator/napari-growth-cone-finder/issues
        Documentation = https://github.com/creator/napari-growth-cone-finder#README.md
        Source Code = https://github.com/creator/napari-growth-cone-finder
        User Support = https://github.com/creator/napari-growth-cone-finder/issues
        These URLs will be displayed on your plugin's napari hub page.
        You may wish to change these before publishing your plugin!
    5. Read the README for more info: https://github.com/napari/napari-plugin-template
    6. We've provided a template description for your plugin page on the napari hub at `.napari-hub/DESCRIPTION.md`.
    You'll likely want to edit this before you publish your plugin.
    7. Consider customizing the rest of your plugin metadata for display on the napari hub:
    https://github.com/chanzuckerberg/napari-hub/blob/main/docs/customizing-plugin-listing.md
```

</details>

:tada: You just created a minimal napari plugin, complete with tests
and ready for automatic deployment! :tada:


```no-highlight
napari-growth-cone-finder
├── .github
|   ├── ISSUE TEMPLATE
|   |   ├── bug_report.yml
│   |   ├── documentation.md
│   |   ├── feature_request.md
│   |   └── task.md
│   ├── workflows
│   |   └── test_and_deploy.yml
|   ├── PULL_REQUEST_TEMPLATE.md
│   └── dependabot.yml
├── .napari-hub
│   ├── DESCRIPTION.md
|   └── config.yml
├── src
│   └── napari_growth_cone_finder
│       ├── _tests
│       │   ├── __init__.py
│       │   └── test_widget.py
│       ├── __init__.py
│       ├── napari.yaml
│       └── _widget.py
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── MANIFEST.in
├── pyproject.toml
├── README.md
└── tox.ini
```


### Step 4: Initialize a git repository in your source code

After Step 3, your system has a file tree in a directory with the source files for your package.
If you haven't already, be sure to [set up Git](https://docs.github.com/en/get-started/git-basics/set-up-git) so that git can be used from the command line or from a GUI such as Github Desktop or VSCode.
This step will initialize the file directory as a git repo and commit your files to the repo. 
When in the command line a single `.` is equivalent to 'perform this action in the current directory'. 
So, `git add .` would stage the changes (i.e., the new file tree) in the current directory to the newly initalized git repo. 
This `.` will be used in other steps, too.

NOTE: This is important not only for version management, but also if you want to
pip install your package locally for testing with `pip install -e .`. (because
the version of your package is managed using git tags,
[see below](#automatic-deployment-and-version-management))

```bash
cd napari-growth-cone-finder
git init
git add .
git commit -m 'initial commit'
```

### Step 5: Upload your repo to GitHub

1. Create a [new repository on GitHub](https://help.github.com/en/github/getting-started-with-github/create-a-repo).

2. Add your newly created GitHub repo as a git remote and push the commited files to GitHub:

   ```bash
   # here, continuing with the example above...
   # but replace with your own username and repo name

   git remote add origin https://github.com/neuronz52/napari-growth-cone-finder.git
   git push -u origin main
   ```

3. You should see your files in the GitHub repo now.

## Understanding and maintaining the generated plugin

### Running tests locally

Tests are automatically setup to run on GitHub when you push changes to your repository.

You may also run your tests locally with [pytest](https://docs.pytest.org/en/7.1.x/).
You'll need to make sure that your package is installed in your environment,
along with testing requirements (specified in the pyproject.toml `[dependency-groups]` section):

```bash
pip install -e ". --groups dev"
pytest
```

### Automated testing and coverage

The repository should already be setup to run your tests each time you push an
update (configuration is in `.github/workflows/test_and_deploy.yml`). You can
monitor them in the "Actions" tab of your github repository. If you're
following along, go have a look... they should be running right now!

Currently, the timeout for these runs is set to 30 minutes to save resources.
You can modify the settings if necessary.
Here you can find information on [GitHub workflows](https://docs.github.com/en/actions/learn-github-actions) and the [timeout parameter](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idtimeout-minutes).

When the tests are done, test coverage will be viewable at
[codecov.io](https://codecov.io/) (assuming your repository is public):
`https://codecov.io/gh/<your-github-username>/<your-package-name>`

You will need to enable the [codecov](https://github.com/apps/codecov) github app
for this to work. See [codecov installation docs](https://github.com/apps/codecov/installations/new)
to install the codecov github app and give it access to your napari plugin repository.

### Set up automatic deployments

Your new package is also nearly ready to automatically deploy to [PyPI]
(whenever you create a tagged release), so that your users can simply `pip install` your package. 
We now use the newer [trusted OIDC publishing](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/) method for PyPI; no API token is needed.

1. If you don't already have one, [create an
   account](https://pypi.org/account/register/) at [PyPI]
2. Verify your email address with PyPI, (if you haven't already) and add
   2FA authentication to your account.
3. Add a new pending publisher. Go to Account Settings > Publishing.
   Scroll down to add a new pending publisher and enter in the requested details.

You are now setup for automatic deployment!

### Automatic deployment and version management

Each time you want to deploy a new version, you just need to create a tagged
commit, and push it to your main branch on github. Your package is set up to
use [setuptools_scm](https://github.com/pypa/setuptools_scm) for version
management, meaning you don't need to hard-code your version anywhere in your
package. It will be inferred from the tag each time you release.

```bash
# the tag will be used as the version string for your package
# make it meaningful: https://semver.org/
git tag -a v0.1.0 -m "v0.1.0"

# make sure to use follow-tags so that the tag also gets pushed to github
git push --follow-tags
```

> Note: as of git 2.4.1, you can set `follow-tags` as default with
> `git config --global push.followTags true`

Monitor the "actions" tab on your github repo for progress... and when the
"deploy" step is finished, your new version should be visible on pypi:

`https://pypi.org/project/<your-package-name>/`

and available for pip install with:

```bash
# for example
pip install napari-growth-cone-finder
```

### Check code style with Pre-commit

This template includes a default yaml configuration for [pre-commit](https://pre-commit.com/).
Among other things, it includes checks for best practices in napari plugins.
You may edit the config at `.pre-commit-config.yaml`

To use it run:

```bash
pip install pre-commit
pre-commit install
```

You can also have these checks run automatically for you when you push to github
by installing [pre-commit ci](https://pre-commit.ci/) on your repository.

### Receive Dependabot notifications about dependencies

This template also includes a default yaml configuration for [Dependabot](https://docs.github.com/en/code-security/dependabot). This can help you check for security updates to easily update vulnerable dependencies.

You will still need to enable Dependabot in your github settings, [see the instructions at this link](https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/configuring-dependabot-security-updates#managing-dependabot-security-updates-for-your-repositories). Your Dependabot configuration file is located at `.github/dependabot.yml`.

### Create your user documentation

Documentation generation is not included in this template.
We recommend following the getting started guides for one of the following documentation generation tools:

1. [Sphinx]
2. [MkDocs]
3. [JupyterBook]

---

## Resources

Please consult the [napari plugin
docs](https://napari.org/stable/plugins/index.html) for more information on
how to create a plugin.

Details on why this plugin template is using the `src` layout can be found [here](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure) and [here](https://hynek.me/articles/testing-packaging/)

## Issues

If you encounter any problems with this template, please
[file an issue](https://github.com/napari/napari-plugin-template/issues/new)
along with a detailed description.

## License

Distributed under the terms of the [BSD-3] license, `napari-plugin-template`
is free and open source software.

[napari organization]: https://github.com/napari/
[gitter_badge]: https://badges.gitter.im/Join%20Chat.svg
[gitter]: https://gitter.im/napari/napari-plugin-template?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge "Join Chat on Gitter.im"
[travis_badge]: https://travis-ci.org/napari/napari-plugin-template.svg?branch=main
[travis]: https://travis-ci.org/napari/napari-plugin-template "See Build Status on Travis CI"
[docs_badge]: https://readthedocs.org/projects/napari-plugin-template/badge/?version=latest
[documentation]: https://napari-plugin-template.readthedocs.io/en/latest/ "Documentation"
[copier]: https://github.com/copier-org/copier
[napari]: https://github.com/napari/napari
[npe2]: https://github.com/napari/npe2
[pypi]: https://pypi.org/
[tox]: https://tox.readthedocs.io/en/latest/
[file an issue]: https://github.com/napari/napari-plugin-template/issues
[sphinx]: https://www.sphinx-doc.org/en/master/usage/quickstart.html
[mkdocs]: https://www.mkdocs.org/getting-started/
[jupyterbook]: https://jupyterbook.org/en/stable/start/your-first-book.html
[mit]: http://opensource.org/licenses/MIT
[mpl v2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[bsd-3]: http://opensource.org/licenses/BSD-3-Clause
[gnu gpl v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[gnu lgpl v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[apache v2.0]: http://www.apache.org/licenses/LICENSE-2.0
[travis ci]: https://travis-ci.com/
[appveyor]: http://www.appveyor.com/
[pypa code of conduct]: https://www.pypa.io/en/latest/code-of-conduct/
[osi_certified]: https://opensource.org/trademarks/osi-certified/web/osi-certified-120x100.png
[osi]: https://opensource.org/
[github actions]: https://github.com/features/actions
[new github repository]: https://help.github.com/en/github/getting-started-with-github/create-a-repo
[setuptools_scm]: https://github.com/pypa/setuptools_scm
