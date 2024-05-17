import os
import platform
import shutil
from pathlib import Path

import click

from mfu.utils.general import run_command


@click.command(help="Check the status of the host machine to run all commands",
               short_help="Check the status of the host machine to run all commands")
@click.option('--fix', is_flag=True, help='Try to fix issues on the machine detected by doctor.')
def doctor(fix):
    click.echo(f"Starting the doctor")
    os_system = platform.system()
    os_release = platform.release()
    click.echo(f"You are running: {os_system} {os_release}")
    click.echo("Checking for a package manager")
    if os_system == "Darwin":
        if shutil.which("brew") is not None:
            click.echo(click.style('You\'ve got brew installed. Good job.', fg='green'))
        else:
            click.echo(click.style('You\'re gonna have some issues.', fg='red'))
            if fix:
                command = ['/bin/bash', '-c',
                           '"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"']
                run_command(command)
            else:
                click.echo('Run with --fix to install it here')
    elif os_system == "Windows":
        if shutil.which("choco") is not None:
            click.echo(click.style('You\'ve got choco installed. Good job.', fg='green'))
        else:
            click.echo(click.style('You\'re gonna have some issues.', fg='red'))
            command = "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
            click.echo(click.style(f'Run this to install:\n{command}', fg='red'))
    elif os_system == "Linux":
        click.echo(click.style('Let\'s be real there is probably a package manager on your machine.', fg='green'))

    click.echo("Checking if kubectl is installed on the machine")
    if shutil.which("kubectl") is not None:
        click.echo(click.style('You\'ve got kubectl installed. Good job.', fg='green'))
    else:
        click.echo(click.style('You\'re gonna have some issues without kubectl.', fg='red'))
        if os_system == "Windows":
            command = 'choco install kubernetes-cli'
            click.echo(click.style(f'Run this to install:\n{command}', fg='red'))
        else:
            if fix:
                if os_system == "Darwin":
                    command = ['brew', 'install', 'kubectl']
                    click.echo(click.style('Attempting to install kubectl.', fg='red'))
                    run_command(command)
                elif os_system == "Linux":
                    command = [
                        'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" > /usr/local/bin/kubectl']
                    click.echo(click.style('Attempting to install kubectl.', fg='red'))
                    run_command(command)
            else:
                click.echo('Run with --fix to install it here')

    click.echo("Checking if kubeconfig file is on the machine")
    if os.path.isfile(f'{Path.home()}/.kube/config'):
        click.echo(click.style('You\'ve got a kubeconfig file. Good Job.', fg='green'))
        click.echo(
            click.style('It doesn\'t mean you\'re out of the woods though. It is possible for the config to be broken',
                        fg='green'))
    else:
        click.echo(click.style('It doesn\'t look like you have a kubeconfig file.', fg='red'))
        click.echo(click.style('You should download one from https://rancher.acumensoft.net/', fg='red'))
