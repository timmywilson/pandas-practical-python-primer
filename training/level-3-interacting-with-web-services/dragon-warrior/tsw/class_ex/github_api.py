"""
Web Services DocString Stub

homework for Wednesday
Function takes 2 parameters instead of 1 - username and specific repo name
Return the issues for that repo



    # use square brackets when referencing a dictionary key.
    # user comes from the json dictionary method from the response object
     # username is referenced as a string in the function def
     # since it's a string, we use format
"""

import requests
from configuration_panda import ConfigurationPanda

credentials = ConfigurationPanda(['PROGRAM_CREDENTIALS'])

class Github:
    """
    Provides access to the Github API

    Class Attributes:
        urls: Github API url templates for accessing various functionality

    Attributes:
        oauth_token: A valid OAuth oauth_token for access the API

    Methods
        user_info: Provide information on a given Github user
        user_repos: Provide info on a given user's repos
        repo_issues: Provide info on a given repo's issues
    """
    urls = requests.get("https://api.github.com").json()

    def __init__(self, oauth_token: str):
        self.oauth_token = oauth_token

    def user_info(self, username: str) -> requests.Response:
        """
        Obtain information about a given user in Github

        Args:
            username: A str specifying a valid Github username

        Returns:
            A reqest.Response object
        """
        url = self.urls['user_url'].format(user=username)
        return requests.get(url)

    def user_repos(self, username: str) -> requests.Response:
        """
        Obtain a list of repos owned by a given user
        Args:
            username: a str specifying a valid Github username

        Returns:
            A request.Response object
        """
        url = self.urls['user_url'].format(user=username) + "/repos"
        return requests.get(url)

    def repo_issues(self, username: str, repo_name: str):
        """A good docstring"""
        url = (
            self.urls['repository_url'].format(
            owner=username, repo=repo_name) + "/issues")
        return requests.get(url)

    def create_issue(self, username: str, repo_name: str,
                     title: str, body: str=None,
                     assignee: str=None, milestone: str=None,
                     labels: list=None) -> requests.Response:
        """

        Args:
            username:
            repo_name:
            title:
            body:
            assignee:
            milestone:
            labels:

        Returns:

        """
        if labels is None:
            labels = []

        headers = {'Authorization': 'token {}'.format(self.oauth_token)}
        url = (
            self.urls['repository_url'].format(
            owner=username, repo=repo_name) + "/issues")
        payload = {
            "title": title, "body": body, "assignee": assignee,
            "milestone": milestone, "labels": labels
        }
        return requests.post(url, headers=headers, json=payload)


    def update_issue(self, username: str, repo_name: str, issue_number: int,
                     title: str, body: str=None,
                     assignee: str=None, state: str=None, milestone: str=None,
                     labels: list=None) -> requests.Response:
        """

        Args:
            username:
            repo_name:
            title:
            body:
            assignee:
            milestone:
            labels:

        Returns:

        """

        if labels is None:
            labels = []

        headers = {'Authorization': 'token {}'.format(self.oauth_token)}
        url = (
            self.urls['repository_url'].format(
            owner=username,
                repo=repo_name) + "/issues/" + str(issue_number))
        payload = {
            "title": title, "body": body, "assignee": assignee,
            "milestone": milestone, "labels": labels
        }
        if state is not None:
            payload['state'] = state

        return requests.patch(url, headers=headers, json=payload)


if __name__ == '__main__':
    #print(credentials.tokens)
    #github_info = github_entry_point()
    ##import pprint
    ##pprint.pprint(github_user_info("timmywilson").json())
    github = Github(oauth_token=credentials.tokens['github'])
    new_issue = github.create_issue (
        username='bigfatpanda-training',
        repo_name='pandas-practical-python-primer',
        title='Example Issue' )

    updated_issue = github.update_issue(
        username='bigfatpanda-training',
        repo_name='pandas-practical-python-primer',
        title='An Updated Example Issue',
        issue_number=new_issue.json()['number'],
        body='This is my updated issue',
        assignee='timmywilson',
        labels=["label1","label2"]
    )