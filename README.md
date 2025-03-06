# napari-plugin-template

[![Test plugin template](https://github.com/napari/napari-plugin-template/actions/workflows/test.yml/badge.svg)](https://github.com/napari/napari-plugin-template/actions/workflows/test.yml)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/napari.svg)](https://python.org)  <!-- Use the versions supported by napari core -->
[![License](https://img.shields.io/pypi/l/napari.svg)](https://github.com/napari/napari-plugin-template/raw/main/LICENSE)

**napari-plugin-template** is a convenient [copier](https://copier.readthedocs.io/en/stable/) template for authoring ([npe2](https://github.com/napari/npe2)-based) [napari](https://napari.org/) plugins.

Creating a plugin is a great way to extend napari's functionality. This repo provides a template to
simplify the development and distribution your plugin. After creating a new plugin, we encourage you to send a
post on our [Zulip forum](napari.zulipchat.com) to notify the napari community.

---

📣 **NOTE: This repo is not meant to be cloned/forked directly!** Instead, the copier application will be used to execute
the template and ask you for configuration information (or you may accept the template's sensible defaults).
Please read [Getting Started](#getting-started) below. 📣

---

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

## Getting Started

These instructions will walk you through how to create a napari plugin. It uses an application called copier
to prompt you for configuration input and does the work of creating a functioning, distributable plugin from your
source code.

### Step 1: Install the template tools.

This step installs the [Copier](https://copier.readthedocs.io/en/stable/) application and the [jinja2-time](https://pypi.org/project/jinja2-time/) extension.
It also installs the napari plugin engine [npe2](https://github.com/napari/npe2), to help validate your new plugin is configured correctly.

Using `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install copier jinja2-time npe2
```

### Step 2: Create a new napari plugin project.
 
The next command will use copier to use the napari-plugin-template to generate a new napari plugin project:

```bash
copier copy --trust https://github.com/napari/napari-plugin-template <new-plugin-name>
```

For example, if you want to create a new plugin with the name, `napari-growth-cone-finder`, you would enter:

```bash
copier copy --trust https://github.com/napari/napari-plugin-template napari-growth-cone-finder
```

Copier will create a new folder in your current working directory named `napari-growth-cone-finder`.
It will also prompt you to begin entering configuration information.

### Step 3: Enter plugin configuration information.

Copier prompts you to enter information about your plugin. For more detailed information on each prompt see
the [prompts reference](./PROMPTS.md).

<details open>
<summary>Configuration prompts</summary>

```sh
copier copy --trust https://github.com/napari/napari-plugin-template napari-growth-cone-finder

🎤 The name of your plugin
   napari-growth-cone-finder
🎤 Display name for your plugin
   Growth Cone Finder
🎤 Plugin module name
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
🎤 Use git tags for versioning?
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
    # you probably want to install your new package into your env
    pip install -e .

    2. Create a github repository with the name 'napari-growth-cone-finder':
    https://github.com/creator/napari-growth-cone-finder.git
    3. Add your newly created github repo as a remote and push:
        git remote add origin https://github.com/creator/napari-growth-cone-finder.git
        git push -u origin main
    4. The following default URLs have been added to `setup.cfg`:
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
napari-growth-cone-finder/
│
├── .github
│   └── workflows
│      └── test_and_deploy.yml
├── LICENSE
├── MANIFEST.in
├── napari_growth_cone_finder
│   ├── __init__.py
│   ├── _widget.py
│   ├── _reader.py
│   ├── napari.yaml
│   └── _tests
│       ├── __init__.py
│       ├── test_widget.py
│       └── test_reader.py
├── pyproject.toml
├── README.md
├── setup.cfg
└── tox.ini
```


### Initialize a git repository in your package

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

### Upload it to github

1. Create a [new github repository]

2. Add your newly created github repo as a remote and push:

   ```bash
   # here, continuing with the example above...
   # but replace with your own username and repo name

   git remote add origin https://github.com/neuronz52/napari-growth-cone-finder.git
   git push -u origin main
   ```

### Monitor testing and coverage

The repository should already be setup to run your tests each time you push an
update (configuration is in `.github/workflows/test_and_deploy.yml`). You can
monitor them in the "Actions" tab of your github repository. If you're
following along, go have a look... they should be running right now!

Currently, the timeout for these runs is set to 30 minutes to save resources. You can modify the settings if necessary. Here you can find information on [GitHub workflows](https://docs.github.com/en/actions/learn-github-actions) and the [timeout parameter](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idtimeout-minutes).

When the tests are done, test coverage will be viewable at
[codecov.io](https://codecov.io/) (assuming your repository is public):
`https://codecov.io/gh/<your-github-username>/<your-package-name>`

You will need to enable the [codecov](https://github.com/apps/codecov) github app
for this to work. See [here](https://github.com/apps/codecov/installations/new)
to install the codecov github app and give it access to your napari plugin repository.

### Set up automatic deployments

Your new package is also nearly ready to automatically deploy to [PyPI]
(whenever you create a tagged release), so that your users can simply `pip install` your package. You just need to create an [API token to authenticate
with PyPi](https://pypi.org/help/#apitoken), and then add it to your github
repository:

1. If you don't already have one, [create an
   account](https://pypi.org/account/register/) at [PyPI]
2. Verify your email address with PyPI, (if you haven't already)
3. Generate an [API token](https://pypi.org/help/#apitoken) at PyPi: In your
   [account settings](https://pypi.org/manage/account/) go to the API tokens
   section and select "Add API token". Make sure to copy it somewhere safe!
4. [Create a new encrypted
   secret](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets#creating-encrypted-secrets)"
   in your github repository with the name "TWINE_API_KEY", and paste in your
   API token.

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

### Running tests locally

Tests are automatically setup to run on github when you push to your repository.

You can run your tests locally with [pytest](https://docs.pytest.org/en/7.1.x/).
You'll need to make sure that your package is installed in your environment,
along with testing requirements (specified in the setup.cfg `extras_require` section):

```bash
pip install -e ".[testing]"
pytest
```

### Create your documentation

Documentation generation is not included in this template.
We recommend following the getting started guides for one of the following documentation generation tools:

1. [Sphinx]
2. [MkDocs]
3. [JupyterBook]

### Pre-commit

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

## Dependabot

This template also includes a default yaml configuration for [Dependabot](https://docs.github.com/en/code-security/dependabot). This can help you check for security updates to easily update vulnerable dependencies.

You will still need to enable Dependabot in your github settings, [see the instructions at this link](https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/configuring-dependabot-security-updates#managing-dependabot-security-updates-for-your-repositories). Your Dependabot configuration file is located at `.github/dependabot.yml`.

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

## Using uv for getting started

:bulb: **Optional** :bulb:

[uv](https://docs.astral.sh/uv/) can reduce complexity since it will automatically install and manage a version of Python.

If you prefer using uv, the following commands are used for getting started:

```bash
uv venv
source .venv/bin/activate
uv pip install copier jinja2-time npe2
uv run copier copy --trust https://github.com/napari/napari-plugin-template <new-plugin-name>
```

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
