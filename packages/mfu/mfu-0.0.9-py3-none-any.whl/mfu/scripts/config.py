import configparser
import os
from pathlib import Path

import click

from mfu.utils.general import write_config_file


@click.command(help="Write default config file",
               short_help="Write default config file")
@click.option('--overwrite', is_flag=True, help='Overwrite existing config file if one exists')
def config(overwrite):
    default_config = configparser.ConfigParser()
    default_config["credentials.forcelink"] = {
        "subdomain": "",
        "forcelinkPasswordPrefix": "",
        "schema": "",
    }
    default_config["credentials.gitlab"] = {
        "token": "",
        "gitlab_url": "",
    }
    default_config["config.forcelink"] = {
        "statuses_to_delete": "RSS,CAS,CL,CA",
    }

    if os.path.isfile(f'{Path.home()}/.mfu'):
        if overwrite:
            write_config_file(default_config)
        else:
            click.echo(click.style(f'File already exists at: {Path.home()}/.mfu', fg='red'))
            click.echo(click.style(f'If you would like to overwrite the file use the --overwrite flag', fg='red'))
    else:
        write_config_file(default_config)
        click.echo(click.style(f'File written to: {Path.home()}/.mfu', fg='green'))
