
from typing import List

from logging import Logger
from logging import getLogger

from github import Github
from github.Milestone import Milestone
from github.PaginatedList import PaginatedList
from github.Repository import Repository

from wx import ALIGN_RIGHT
from wx import ALIGN_TOP
from wx import ALL
from wx import BU_LEFT
from wx import CB_DROPDOWN
from wx import CB_READONLY
from wx import EVT_COMBOBOX
from wx import EVT_LISTBOX
from wx import EXPAND
from wx import HORIZONTAL
from wx import LB_MULTIPLE
from wx import LB_OWNERDRAW
from wx import LB_SINGLE
from wx import VERTICAL

from wx import Button
from wx import CommandEvent
from wx import StaticBoxSizer
from wx import ListBox
from wx import BoxSizer
from wx import ComboBox
from wx import Window

from wx import NewIdRef as wxNewIdRef

from gittodoistclone.general.Preferences import Preferences

from gittodoistclone.ui.BasePanel import BasePanel


class GitHubPanel(BasePanel):

    PROPORTION_NOT_CHANGEABLE: int = 0
    PROPORTION_CHANGEABLE:     int = 1

    ALL_ISSUES_INDICATOR:     str = 'All'
    OPEN_MILESTONE_INDICATOR: str = 'Open'
    OPEN_ISSUE_INDICATOR:     str = 'open'

    def __init__(self, parent: Window):

        super().__init__(parent)

        self.SetBackgroundColour(self.backgroundColor)

        self.logger:      Logger       = getLogger(__name__)
        self._preferences: Preferences = Preferences()

        githubToken:  str    = self._preferences.githubApiToken
        self._github: Github = Github(githubToken)

        contentSizer: BoxSizer = self._layoutContent()

        self.SetSizer(contentSizer)
        self.Fit()

    def _layoutContent(self) -> BoxSizer:

        sizer: BoxSizer = BoxSizer(VERTICAL)

        rz: StaticBoxSizer = self._createRepositorySelection()
        mz: StaticBoxSizer = self._createMilestoneSelection()
        iz: StaticBoxSizer = self._createIssueSelection()
        bz: BoxSizer       = self._createCloneButton()

        sizer.Add(rz, GitHubPanel.PROPORTION_NOT_CHANGEABLE, ALL | EXPAND, 1)
        sizer.Add(mz, GitHubPanel.PROPORTION_CHANGEABLE, ALL | EXPAND, 2)
        sizer.Add(iz, GitHubPanel.PROPORTION_CHANGEABLE, ALL | EXPAND | ALIGN_TOP, 1)
        sizer.Add(bz, GitHubPanel.PROPORTION_NOT_CHANGEABLE, ALL | ALIGN_RIGHT, 2)

        sizer.Fit(self)

        return sizer

    def _createRepositorySelection(self) -> StaticBoxSizer:

        repoSelectionWxId: int = wxNewIdRef()

        self._repositorySelection: ComboBox = ComboBox(self, repoSelectionWxId, style=CB_DROPDOWN | CB_READONLY)

        sz = StaticBoxSizer(VERTICAL, self, "Repository List")
        sz.Add(self._repositorySelection, GitHubPanel.PROPORTION_NOT_CHANGEABLE, EXPAND)

        self.__populateRepositories()

        self.Bind(EVT_COMBOBOX, self._onRepositorySelected, id=repoSelectionWxId)

        return sz

    def _createMilestoneSelection(self) -> StaticBoxSizer:

        milestoneSelectionWxId: int = wxNewIdRef()

        self._milestoneList: ListBox = ListBox(self,  milestoneSelectionWxId, style=LB_SINGLE | LB_OWNERDRAW)

        self._milestoneList.Enable(False)
        sz = StaticBoxSizer(VERTICAL, self, "Repository Milestone Titles")
        sz.Add(self._milestoneList, GitHubPanel.PROPORTION_CHANGEABLE, EXPAND)

        self.Bind(EVT_LISTBOX, self._onMilestoneSelected, milestoneSelectionWxId)

        return sz

    def _createIssueSelection(self) -> StaticBoxSizer:

        issueWxID: int = wxNewIdRef()

        self._issueList: ListBox = ListBox(self,  issueWxID, style=LB_MULTIPLE | LB_OWNERDRAW)

        self._issueList.Enable(False)
        sz = StaticBoxSizer(VERTICAL, self, "Repository Issues")
        sz.Add(self._issueList, GitHubPanel.PROPORTION_CHANGEABLE, EXPAND)

        return sz

    def _createCloneButton(self) -> BoxSizer:

        bSizer:     BoxSizer = BoxSizer(HORIZONTAL)
        fqFileName: str = BasePanel.retrieveResourcePath('play.png')

        cloneWxID: int = wxNewIdRef()

        self._cloneButton: Button = Button(self, id=cloneWxID, style=BU_LEFT, label='Clone')

        self._cloneButton.Enable(False)
        bSizer.Add(self._cloneButton, GitHubPanel.PROPORTION_NOT_CHANGEABLE, ALL, 1)

        return bSizer

    def _onRepositorySelected(self, event: CommandEvent):

        repoName: str = event.GetString()
        self.logger.info(f'{repoName=}')

        self.__populateMilestones(repoName)

    def _onMilestoneSelected(self, event: CommandEvent):

        repoName:      str = self._repositorySelection.GetStringSelection()
        milestoneTitle: str = event.GetString()
        self.logger.info(f'{repoName=} - {milestoneTitle=}')

        self.__populateIssues(milestoneTitle, repoName)

    def __populateRepositories(self):

        repos: PaginatedList = self._github.search_repositories(query='user:hasii2011')    # TODO get user name from preferences

        repoNames: List[str] = []
        for repository in repos:
            repoNames.append(repository.full_name)

        self._repositorySelection.SetItems(repoNames)

    def __populateMilestones(self, repoName):

        repo:            Repository  = self._github.get_repo(repoName)
        mileStones:      PaginatedList = repo.get_milestones(state=GitHubPanel.OPEN_MILESTONE_INDICATOR)

        mileStoneTitles: List[str] = [GitHubPanel.ALL_ISSUES_INDICATOR]

        for mileStone in mileStones:
            mileStoneTitles.append(mileStone.title)

        self._milestoneList.SetItems(mileStoneTitles)
        self._milestoneList.Enable(True)

    def __populateIssues(self, milestoneTitle, repoName):

        repo:        Repository    = self._github.get_repo(repoName)
        open_issues: PaginatedList = repo.get_issues(state=GitHubPanel.OPEN_ISSUE_INDICATOR)

        issueTitles: List[str] = []

        if milestoneTitle == GitHubPanel.ALL_ISSUES_INDICATOR:
            for issue in open_issues:
                issueTitles.append(issue.title)
        else:
            for issue in open_issues:
                mileStone: Milestone = issue.milestone
                if mileStone is not None and mileStone.title == milestoneTitle:
                    issueTitles.append(issue.title)

        self._issueList.SetItems(issueTitles)
        self._issueList.Enable(True)
        self._cloneButton.Enable(True)