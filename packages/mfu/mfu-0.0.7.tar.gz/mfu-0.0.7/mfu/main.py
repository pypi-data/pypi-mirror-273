import click
from .scripts.sync import sync
from .scripts.doctor import doctor
# from .scripts.cluster import cluster
# from .scripts.config import config


@click.group(help="Michael\'s fun utilities")
def cli():
    pass


cli.add_command(sync)
cli.add_command(doctor)
# cli.add_command(cluster)
# cli.add_command(config)
