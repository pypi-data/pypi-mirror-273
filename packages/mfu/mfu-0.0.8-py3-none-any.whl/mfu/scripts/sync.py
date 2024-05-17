import os
import platform
import shutil
from pathlib import Path

import click
from git import Repo
from kubernetes import client, config
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from mfu.utils.general import run_command


@click.group(help="Command group to sync files to kubernetes pods",
             short_help="Command group to sync files to kubernetes pods")
def sync():
    pass


@sync.command(help="Run as a background process and write detected file changes to the forcelink-webapp pod",
              short_help="Run as a background process and write detected file changes to the forcelink-webapp pod")
@click.option('--path', default=os.getcwd(), help='The path on which to listen for file changes')
@click.option('--context', default='core', help='Kubernetes context of the cluster that the pod is running in')
@click.option('--podlabel', default='app.kubernetes.io/instance=webapp-forcelink',
              help='Label on which to match the running forcelink pod')
@click.option('--podroot', default='/usr/local/tomcat/webapps/forcelink',
              help='The path within the pod that maps to the local path root.')
def listen(path, context, podlabel, podroot):
    config.load_kube_config(context=context)
    v1 = client.CoreV1Api()

    class Handler(FileSystemEventHandler):
        def __init__(self, project_path, branch):
            self.project_path = project_path.replace("\\", "/")  # Remove windows mapping for pod
            self.branch = branch.lower()
            self.system = platform.system()

        def on_modified(self, event):
            if "WebContent" in event.src_path and "~" not in event.src_path and not event.is_directory:
                pods = v1.list_namespaced_pod(f"acumen-{self.branch}", label_selector=podlabel).items
                if pods:
                    pod = pods[0]
                    pod_name = pod.metadata.name
                    src_path = event.src_path.replace("\\", "/")
                    dest_path = src_path.replace(self.project_path + "/WebContent", "")
                    if self.system == "Windows":
                        Path(f"{Path.home()}/.mfu-temp/").mkdir(parents=True, exist_ok=True)
                        copy_path = f"{Path.home()}\.mfu-temp\{src_path.split('/')[-1]}"
                        click.echo(f"Creating temp file at {copy_path}")
                        shutil.copyfile(src_path, copy_path)
                        src_path = copy_path.replace("\\", "/").split(":")[-1]
                    command = f"kubectl --context={context} --namespace=acumen-{self.branch} cp {src_path} {pod_name}:{podroot}{dest_path}"
                    command_list = command.split(" ")
                    if run_command(command_list) == 0:
                        click.echo(
                            f"Synced: {event.src_path} to {pod_name}:{podroot}{event.src_path.replace(f'{self.project_path}/WebContent', '')}")
                else:
                    click.echo(click.style('No pods were found', fg='red'))
                    click.echo(click.style(f'Search Details:', fg='red'))
                    click.echo(click.style(f'- Namespace: forcelink-{branch_name}', fg='red'))
                    click.echo(click.style(f'- Pod Label: {podlabel}', fg='red'))

    click.echo(f'Starting to listen on: {path}')
    repo = Repo(path)
    branch_name = f"{repo.active_branch}"
    event_handler = Handler(path, branch_name)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()
