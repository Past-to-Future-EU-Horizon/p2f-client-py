# Local libraries
from p2f_pydantic.link_git import Git_Repository
from .conn import health_check
# Third Party Libraries
import requests
# Batteries included libraries
from typing import List, Optional
from uuid import UUID

class git:
    """Class for managing datasets and git repositories they're associated with
    """ 
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "git/"
        self.git_url = self.base_url / self.prefix
    def upload_git(self, new_git_repo: Git_Repository) -> Git_Repository:
        """Upload a git repository to the P2F API

        :param new_git_repo: Git repository to be added to the API
        :type new_git_repo: p2f_pydantic.link_git.Git_Repository
        :return: New git repository as processed by API
        :rtype: p2f_pydantic.link_git.Git_Repository
        """
        if health_check(self.base_url):
            r = requests.post(self.git_url, 
                              data=self.p2fclient.json_serialize_with_auth("new_git_repo", new_git_repo.model_dump_json(exclude_unset=True)),
                              headers={"Content-Type": "application/json"})
            if r.ok:
                return Git_Repository(**r.json())
    def list_git_repositories(self) -> List[Git_Repository]:
        """List the git repositories on the P2F API

        :return: List of git repositories
        :rtype: List[p2f_pydantic.link_git.Git_Repository]
        """
        if health_check(self.base_url):
            r = requests.get(self.git_url, 
                             data=self.p2fclient.json_serialize_with_auth(),
                             headers={"Content-Type": "application/json"})
            if r.ok:
                return [Git_Repository(**x) for x in r.json()]
            else:
                return []
    def get_git_repository(self, git_repo_id: str) -> Git_Repository:
        """Get a specific git repository based on its API git_repo_id

        :param git_repo_id: git repository id from API
        :type git_repo_id: str
        :return: Git_Repository from API
        :rtype: Git_Repository
        """
        if health_check(self.base_url):
            r = requests.get(self.git_url, 
                             data=self.p2fclient.json_serialize_with_auth(), 
                             params={"git_repo_id": git_repo_id}, 
                             headers={"Content-Type": "application/json"})
            if r.ok:
                return Git_Repository(**r.json())
    def delete_git_repository(self, git_repo_id: str):
        """Delete a git repository from the API

        :param git_repo_id: git repository id from the API
        :type git_repo_id: str
        """ 
        if health_check(self.base_url):
            r = requests.delete(self.git_url, 
                                data=self.p2fclient.json_serialize_with_auth(), 
                                params={"git_repo_id": git_repo_id},
                                headers={"Content-Type": "application/json"})
    def assign_git_repository(self, git_repo_id: str, dataset_id: str):
        """Assign a git repository to a dataset by git_repo_id and dataset_id

        :param git_repo_id: git repository id from API
        :type git_repo_id: str
        :param dataset_id: dataset id from API
        :type dataset_id: str
        """
        assign_url = self.git_url / "assign"
        assign_url.args["git_repo_id"] = git_repo_id
        assign_url.args["dataset_id"] = dataset_id
        if health_check(self.base_url):
            r = requests.post(assign_url, 
                              data=self.p2fclient.json_serialize_with_auth(), 
                              headers={"Content-Type": "application/json"})
    def remove_git_repository(self, git_repo_id: str, dataset_id: str):
        """Remove a git repository assigned to a dataset by git_repo_id and dataset_id

        :param git_repo_id: git repository id from API
        :type git_repo_id: str
        :param dataset_id: dataset id from API
        :type dataset_id: str
        """
        assign_url = self.git_url / "remove"
        assign_url.args["git_repo_id"] = git_repo_id
        assign_url.args["dataset_id"] = dataset_id
        if health_check(self.base_url):
            r = requests.post(assign_url, 
                              data=self.p2fclient.json_serialize_with_auth(), 
                              headers={"Content-Type": "application/json"})