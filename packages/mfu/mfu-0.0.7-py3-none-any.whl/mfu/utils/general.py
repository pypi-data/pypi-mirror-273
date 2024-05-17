import configparser
import datetime
import hashlib
import os
import subprocess
from pathlib import Path

import click
import gitlab
import requests

from .forcelink import login


def get_config_file():
    config = configparser.ConfigParser()
    if os.path.isfile(f'{Path.home()}/.mfu'):
        config.read(f'{Path.home()}/.mfu')
    return config


def write_config_file(config):
    with open(f'{Path.home()}/.mfu', 'w') as configfile:
        config.write(configfile)


def get_config_file_section(section):
    config = get_config_file()
    if section in config:
        return config[section]
    else:
        raise Exception(f"You're configuration file does not have a {section} section")


def run_command(command_list):
    try:
        process = subprocess.Popen(
            command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        result = process.communicate()
        if process.returncode == 0:
            return process.returncode
        else:
            click.echo(click.style('There was an error running your command.', fg='red'))
            click.echo(click.style(f'{result}', fg='red'))
            return process.returncode
    except subprocess.CalledProcessError as ex:
        click.echo(click.style('There was an error running your command.', fg='red'))
        click.echo(click.style(f'{ex}', fg='red'))
        return 1


def login_to_forcelink():
    session = requests.Session()
    section = get_config_file_section('credentials.forcelink')
    subdomain = section['subdomain']
    forcelinkPasswordPrefix = section['forcelinkPasswordPrefix']
    schema = section['schema']
    passwordT = forcelinkPasswordPrefix + datetime.datetime.now().strftime("%d%m%Y")
    password = hashlib.md5(passwordT.encode("utf-8")).hexdigest()

    try:
        login(session, "forcelink", password, schema, subdomain)
        return session
    except Exception as e:
        raise Exception("Could not log you in. Please check user and that the server is up.")


def get_gitlab_api():
    section = get_config_file_section('credentials.gitlab')
    token = section['token']
    gitlab_url = section['gitlab_url']
    return gitlab.Gitlab(url=gitlab_url, private_token=token)


def compare_metrics(branch_to_check, project):
    try:
        comparison = project.repository_compare(from_='main', to=branch_to_check, all=True)
        if comparison['commits']:
            oldest_commit = comparison['commits'][0]
            latest_commit = comparison['commits'][-1]
            data = {}
            for commit in comparison['commits']:
                if commit['committer_name'] in data:
                    data[commit['committer_name']] += 1
                else:
                    data[commit['committer_name']] = 1
            return {'oldest_commit': {'author': oldest_commit['author_name'], 'timestamp': oldest_commit['created_at']},
                    'latest_commit': {'author': latest_commit['author_name'], 'timestamp': latest_commit['created_at']},
                    'statistics': data}
        else:
            return {}
    except Exception as e:
        print(e)
