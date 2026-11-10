# Local libraries
from p2f_pydantic.link_git import Git_Repository
from .conn import eval_non_ok_return
# Third Party Libraries
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
        self.data_model = Git_Repository
    def upload_git(self, new_git_repo: Git_Repository) -> Git_Repository:
        """Upload a git repository to the P2F API

        :param new_git_repo: Git repository to be added to the API
        :type new_git_repo: p2f_pydantic.link_git.Git_Repository
        :return: New git repository as processed by API
        :rtype: p2f_pydantic.link_git.Git_Repository
        """
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.post(self.git_url, 
                                data=new_git_repo.model_dump_json(exclude_unset=True))
                if r.ok:
                    return Git_Repository(**r.json())
                else: 
                    eval_non_ok_return(r.status_code)
    def list_git_repositories(self) -> List[Git_Repository]:
        """List the git repositories on the P2F API

        :return: List of git repositories
        :rtype: List[p2f_pydantic.link_git.Git_Repository]
        """
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.get(self.git_url)
                if r.ok:
                    return [Git_Repository(**x) for x in r.json()]
                else: 
                    eval_non_ok_return(r.status_code)
    def get_git_repository(self, git_repo_id: str) -> Git_Repository:
        """Get a specific git repository based on its API git_repo_id

        :param git_repo_id: git repository id from API
        :type git_repo_id: str
        :return: Git_Repository from API
        :rtype: Git_Repository
        """
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.get(self.git_url,
                                params={"git_repo_id": git_repo_id})
                if r.ok:
                    return Git_Repository(**r.json())
                else: 
                    eval_non_ok_return(r.status_code)
    def delete_git_repository(self, git_repo_id: str):
        """Delete a git repository from the API

        :param git_repo_id: git repository id from the API
        :type git_repo_id: str
        """ 
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.delete(self.git_url,
                                    params={"git_repo_id": git_repo_id})
    def assign_git_repository(self, git_repo_id: str, dataset_id: UUID):
        """Assign a git repository to a dataset by git_repo_id and dataset_id

        :param git_repo_id: git repository id from API
        :type git_repo_id: str
        :param dataset_id: dataset id from API
        :type dataset_id: str
        """
        assign_url = self.git_url / "assign"
        assign_url.args["git_repo_id"] = git_repo_id
        assign_url.args["dataset_id"] = str(dataset_id)
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.post(assign_url)
    def remove_git_repository(self, git_repo_id: str, dataset_id: UUID):
        """Remove a git repository assigned to a dataset by git_repo_id and dataset_id

        :param git_repo_id: git repository id from API
        :type git_repo_id: str
        :param dataset_id: dataset id from API
        :type dataset_id: str
        """
        remove_url = self.git_url / "remove"
        remove_url.args["git_repo_id"] = git_repo_id
        remove_url.args["dataset_id"] = str(dataset_id)
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.post(remove_url)