
from logging import Logger
from logging import getLogger

import logging.config

from os import sep as osSep

from json import load as jsonLoad

from pkg_resources import resource_filename

from pathlib import Path

from gittodoistclone.general.Preferences import Preferences
from gittodoistclone.general.Version import Version
from gittodoistclone.ui.ClonerApplication import ClonerApplication


class PyGitIssueClone:

    MADE_UP_PRETTY_MAIN_NAME:     str = "Python Github Issue Clone"

    JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfiguration.json"

    RESOURCES_PACKAGE_NAME: str = 'gittodoistclone.resources'
    RESOURCES_PATH:         str = f'gittodoistclone{osSep}resources'

    RESOURCE_ENV_VAR:       str = 'RESOURCEPATH'

    def __init__(self):

        self._setupSystemLogging()
        self.logger: Logger = getLogger(__name__)

        Preferences.determinePreferencesLocation()
        configFile: Path = Path(Preferences.getPreferencesLocation())
        #
        # Will create a default one if necessary
        #
        if configFile.exists() is False:
            self._preferences = Preferences()

    def startApp(self):

        app: ClonerApplication = ClonerApplication(redirect=False)
        app.MainLoop()

    def displayVersionInformation(self):
        import wx
        import sys
        import platform

        print("Versions: ")
        print(f"PyGitIssueClone:  {Version().applicationVersion}")
        print(f'Platform: {platform.platform()}')
        print(f'    System:       {platform.system()}')
        print(f'    Version:      {platform.version()}')
        print(f'    Release:      {platform.release()}')

        print(f'WxPython: {wx.__version__}')
        print(f'Python:   {sys.version.split(" ")[0]}')

    @classmethod
    def retrieveResourcePath(cls, bareFileName: str) -> str:

        # Use this method in Python 3.9
        # from importlib_resources import files
        # configFilePath: str  = files('org.pyut.resources').joinpath(Pyut.JSON_LOGGING_CONFIG_FILENAME)

        try:
            fqFileName: str = resource_filename(PyGitIssueClone.RESOURCES_PACKAGE_NAME, bareFileName)
        except (ValueError, Exception):
            #
            # Maybe we are in an app
            #
            from os import environ
            pathToResources: str = environ.get(f'{PyGitIssueClone.RESOURCE_ENV_VAR}')
            fqFileName:      str = f'{pathToResources}/{PyGitIssueClone.RESOURCES_PATH}/{bareFileName}'

        return fqFileName

    def _setupSystemLogging(self):

        configFilePath: str = PyGitIssueClone.retrieveResourcePath(PyGitIssueClone.JSON_LOGGING_CONFIG_FILENAME)

        with open(configFilePath, 'r') as loggingConfigurationFile:
            configurationDictionary = jsonLoad(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads   = False


if __name__ == "__main__":

    print(f"Starting {PyGitIssueClone.MADE_UP_PRETTY_MAIN_NAME}")

    issueCloner: PyGitIssueClone = PyGitIssueClone()
    issueCloner.displayVersionInformation()
    issueCloner.startApp()
