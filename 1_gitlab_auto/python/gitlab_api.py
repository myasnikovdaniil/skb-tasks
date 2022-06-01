import gitlab
import config
from log import logger

gl = gitlab.Gitlab(url = config.gitlab_URL,
                   private_token = config.gitlab_TOKEN)

def get_all_branches() -> list:
    """
    Retrieves all branches from all projects in Gitlab
    """
    projects = gl.projects.list(all=True)
    all_branches = []
    for project in projects:
        branches = project.branches.list()
        all_branches.extend(branches)
    return all_branches