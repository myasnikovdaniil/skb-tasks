#!/bin/python3.9
import datetime
import re
import gitlab
from time import sleep
from cache import read_local_cache, write_local_cache
from gitlab_api import get_all_branches
from email_send import send_emails
from log import logger
from config import  branch_correct_names, \
                    branch_name_regexp, \
                    stale_period, \
                    cache_file_name, \
                    gitlab_URL, \
                    gitlab_TOKEN, \
                    gitlab_check_interval, \
                    smtp_server, \
                    smtp_server_port, \
                    source_email, \
                    smtp_pass

def check_branch_naming(
    project_branch: gitlab.v4.objects.branches.ProjectBranch,
    branch_correct_names: list,
    branch_name_regexp: str,
    ) -> bool:
    """
    Check branch naming with dictionary of correct names
    and regexp, that define correct format
    """
    if project_branch.name in branch_correct_names\
        or re.match(branch_name_regexp, project_branch.name) is not None:
        return False
    else:
        return True

def check_branch_staleness(
    project_branch: gitlab.v4.objects.branches.ProjectBranch,
    stale_period: int = 14
    ) -> bool:
    """
    Check branch staleness
    """
    delta = datetime.timedelta(days=stale_period)
    committed_date = datetime.datetime.fromisoformat(
                        project_branch.attributes['commit']['committed_date'])
    current_time = datetime.datetime.now(datetime.timezone.utc)
    if current_time - committed_date < delta:
        return False
    else:
        return True
def main():
    # Main logic
    all_branches = get_all_branches()
    cache = read_local_cache(cache_file_name)
    emails_list = []
    for branch in all_branches:
        # Default for not skipping 
        cache_entry = {
            'skip_rename_warn': False,
            'skip_update_warn': False,
            }
        try:
            cache_entry = cache[branch.attributes['web_url']]
        except KeyError:
            pass
        if check_branch_naming(branch, branch_correct_names, branch_name_regexp)\
            and not cache_entry['skip_rename_warn']:
            emails_list.append({
                'dst_email': branch.attributes['commit']['committer_email'],
                'template': 'rename',
                'branch': branch.attributes['web_url'],
            })
            if cache.get(branch.attributes['web_url']) is not None:
                cache[branch.attributes['web_url']].update(skip_rename_warn = True)
            else:
                cache[branch.attributes['web_url']] = {'skip_rename_warn': True}
        if check_branch_staleness(branch, stale_period)\
            and not cache_entry['skip_update_warn']:
            emails_list.append({
                'dst_email': branch.attributes['commit']['committer_email'],
                'template': 'update',
                'branch': branch.attributes['web_url'],
            })
            if cache.get(branch.attributes['web_url']) is not None:
                cache[branch.attributes['web_url']].update(skip_update_warn = True)
            else:
                cache[branch.attributes['web_url']] = {'skip_update_warn': True}
    send_emails(emails_list)
    write_local_cache(cache_file_name, cache)

    # Statistics info
    logger.info(f'Script have worked with {len(all_branches)} project branches')
    logger.info(f'Script have sent {len(emails_list)} warning emails')
    logger.info(f'Local cache contains {len(cache)} entries')

if gitlab_URL is not None \
    and gitlab_TOKEN is not None \
    and smtp_server is not None \
    and smtp_server_port is not None \
    and source_email is not None \
    and smtp_pass is not None:
    while True:
        main()
        sleep(int(datetime.timedelta(hours=gitlab_check_interval).total_seconds()))
else:
    logger.error("Can't start script, missing environment variables")

