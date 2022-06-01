from os import getenv

# Connection settings
gitlab_URL = getenv('GITLAB_URL') 
gitlab_TOKEN = getenv('GITLAB_TOKEN')
# Email settings
smtp_server = getenv('SMTP_SERVER')
smtp_server_port = getenv('SMTP_SERVER_PORT')
source_email = getenv('SOURCE_EMAIL')
smtp_pass = getenv('SMTP_PASS')
tmp_dir = getenv('TMP_DIR', '/tmp')

# Other settings
# interval in hours
gitlab_check_interval = 4
branch_correct_names = [
    'master',
    'main',
    'dev',
    'devel',
]
branch_name_regexp = r'^(feature|bugfix)/task-\d+'
# Period in days, after which the branch considered as staled
stale_period = 14
cache_file_name = f'{tmp_dir}/app_cache.json'
# Email templates
email_rename_templ = """\
Subject: Rename branch in Git

You recieved this message because you are latest committer in {branch},\
please rename it!\
"""
email_update_templ = """\
Subject: Update or delete branch in Git

You recieved this message because you are latest committer in {branch},\
please update or delete it!\
"""