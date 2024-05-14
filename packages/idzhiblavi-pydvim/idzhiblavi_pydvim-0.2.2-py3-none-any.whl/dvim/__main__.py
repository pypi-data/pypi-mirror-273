#!/usr/bin/env python3

import click
from dvim.runner import Runner


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.option("--executable", default="nvim")
@click.option("--workspace", default=None)
@click.option("--session", default=None)
@click.pass_context
def cli(ctx, debug, executable, workspace, session):
    ctx.obj = Runner(debug, executable, workspace, session)


@cli.group()
def execute():
    pass


@execute.command()
@click.pass_context
def ui(ctx):
    ctx.obj.ui()


@cli.group()
def start():
    pass


@start.command()
@click.pass_context
def server(ctx):
    ctx.obj.server()


@start.command()
@click.pass_context
def headless(ctx):
    ctx.obj.headless()


@start.command()
@click.pass_context
def local(ctx):
    ctx.obj.local()


def cli_entrypoint():
    cli()


if __name__ == "__main__":
    cli_entrypoint()
