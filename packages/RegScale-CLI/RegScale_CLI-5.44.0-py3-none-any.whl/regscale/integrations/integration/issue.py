"""
Integration Issue
"""

from abc import ABC, abstractmethod
from typing import Dict, List

from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models import Issue, Vulnerability


class IntegrationIssue(ABC):
    """
    Abstract class for Integration Issue
    """

    def __init__(
        self,
        **kwargs,
    ):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def pull(self):
        """
        Pull inventory from an Integration platform into RegScale
        """

    def create_issues(
        self,
        issues: list[Issue],
    ):
        """
        Create issues in RegScale

        :param list[Issue] issues: list of issues to create
        """
        Issue.batch_create(items=issues)

    @staticmethod
    def close_issues(issue_vuln_map: Dict[int, Dict[int, List[Vulnerability]]]) -> None:
        """
        Close issues in RegScale based on the newest vulnerabilities

        :param Dict[int, Dict[int, List[Vulnerability]]] issue_vuln_map: map of issues to
            vulnerabilities by way of assets!
        """

        update_issues: List[Issue] = []
        for key in issue_vuln_map.keys():
            # close existing_issues in RegScale if they are no longer relevant
            for asset_key in issue_vuln_map[key].keys():
                vulns = issue_vuln_map[key][asset_key]
                if not [vuln for vuln in vulns if vuln.severity.lower() in ["moderate", "high", "critical"]]:
                    # Close issue
                    update_issue = Issue.get_object(object_id=key)
                    if update_issue:
                        update_issue.status = "Closed"
                        update_issue.dateCompleted = get_current_datetime()
                        update_issues.append(update_issue)
        if update_issues:
            Issue.batch_update(items=update_issues)
