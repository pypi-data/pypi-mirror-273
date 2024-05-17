import re

import click
import requests
from kubernetes import client, config

from mfu.utils.general import login_to_forcelink, get_gitlab_api, compare_metrics, get_config_file_section


@click.group(help="Command group of cluster maintenance scripts",
             short_help="Command group of cluster maintenance scripts")
def cluster():
    pass


@cluster.command(help="Compare Git and Forcelink to check owner for all active namespaces",
                 short_help="Compare Git and Forcelink to check owner for all active namespaces")
@click.option('--context', default='core', help='Kubernetes context of the cluster that the pod is running in')
@click.option('--namespace_pattern', default="(?:forcelink-)(dev\d*)",
              help='Kubernetes context of the cluster that the pod is running in')
@click.option('--delete', is_flag=True, help='Deletes marked workorders')
def get_namespace_owners(context, namespace_pattern, delete):
    config.load_kube_config(context=context)
    v1 = client.CoreV1Api()
    user_regex_string = re.compile(namespace_pattern)
    namespaces = []
    for item in v1.list_namespace().items:
        match = re.match(user_regex_string, item.metadata.name)
        if match:
            namespaces.append(match.group(1))

    session = login_to_forcelink()
    branches = []
    total_namespaces = len(namespaces)
    gl = get_gitlab_api()
    project = gl.projects.get(16)
    for index, code in enumerate(namespaces):
        print(f"Getting Data for {code} - {index + 1}/{total_namespaces}")
        requests.packages.urllib3.disable_warnings()
        response = session.get(f'https://za2.forcelink.net/forcelink/rest/workordermanager/getByCodeJson?code={code}',
                               verify=False)
        error_list = []
        try:
            data = response.json()
            obj = {'statusCode': data['statusCode'],
                   'code': data['code'],
                   'statusDescription': data['statusDescription'],
                   'allocatedToText': data['allocatedToText'],
                   'systemStatusId': data['systemStatusId'],
                   'systemStatus': data['systemStatus']
                   }
            branches.append(obj)
        except Exception as e:
            print(e)
            error_list.append(code)

    item_list = []
    for item in sorted(branches, key=lambda d: (d['statusCode'], d['allocatedToText'])):
        item.pop('systemStatusId')
        item_list.append(item)

    print("Items that should be deleted")
    branches = sorted(branches, key=lambda d: (d['statusCode'], d['allocatedToText']))
    deleteable_branches = []
    for item in branches:
        # if item['statusCode'] in get_config_file_section("config.forcelink")\
        #         .get("statuses_to_delete", "RSS,CAS,CL,CA").split(','):
        if item['statusCode'] in "CAS,CADC,RSS".split(','):
            deleteable_branches.append(item['code'])
        try:
            metrics = compare_metrics(item['code'], project)
            if 'latest_commit' in metrics:
                print(f"{item['code']} - {item['statusCode']} {item['statusDescription']} - {item['allocatedToText']} - {metrics['latest_commit']}")
            else:
                print(f"{item['code']} - {item['statusDescription']} - {item['allocatedToText']} - {metrics}")
        except Exception as e:
            print(e)

    if delete:
        print(deleteable_branches)
        for branch_code in deleteable_branches:
            print(f"Deleting branch: {branch_code}")
            try:
                project.branches.get(branch_code).delete()
            except Exception as e:
                print(e)



@cluster.command(help="Get branch_metrics", short_help="Get branch_metrics")
@click.option('--branch', default=None, help='Specific branch to check metrics on')
def branch_metrics(branch):
    gl = get_gitlab_api()
    project = gl.projects.get(16)
    branches = []
    if branch is None:
        branches = project.branches.list(get_all=True)
    else:
        branches = [project.branches.get(branch)]
    for branch in branches:
        print(compare_metrics(branch.name, project))
