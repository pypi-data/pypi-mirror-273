import click

from komo.lambda_labs.connect import connect


@click.command("connect")
def cmd_connect():
    api_key = click.prompt("Please enter your Lambda Labs API Key")
    connect(api_key)
