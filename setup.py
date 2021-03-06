"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['PyGitIssueClone.py']
DATA_FILES = [('gittodoistclone/resources', ['gittodoistclone/resources/loggingConfiguration.json']),
              ('gittodoistclone/resources', ['gittodoistclone/resources/play.png']),
              ('gittodoistclone/resources', ['gittodoistclone/resources/version.txt']),
              ('gittodoistclone/resources', ['gittodoistclone/resources/packageversions.txt'])
              ]
OPTIONS = {}

setup(
    app=APP,
    data_files=DATA_FILES,
    packages=['gittodoistclone',
              'gittodoistclone.general',
              'gittodoistclone.general.exceptions',
              'gittodoistclone.ui',
              'gittodoistclone.ui.dialogs'
              ],
    include_package_data=True,
    zip_safe=False,

    url='https://github.com/hasii2011/gittodoistclone',
    author='Humberto A. Sanchez II',
    author_email='Humberto.A.Sanchez.II@gmail.com',
    description='Clone Github issues in Todoist',
    options={},
    setup_requires=['py2app'],
    install_requires=['wxPython', 'PyGithub', 'todoist-python']
)
