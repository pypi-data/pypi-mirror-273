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
@click.argument('args', nargs=-1, type=str)
@click.pass_context
def ui(ctx, args):
    ctx.obj.ui(args)


@cli.group()
def start():
    pass


@start.command()
@click.argument('args', nargs=-1, type=str)
@click.pass_context
def server(ctx, args):
    ctx.obj.server(args)


@start.command()
@click.argument('args', nargs=-1, type=str)
@click.pass_context
def headless(ctx, args):
    ctx.obj.headless(args)


@start.command()
@click.argument('args', nargs=-1, type=str)
@click.pass_context
def local(ctx, args):
    ctx.obj.local(args)


def cli_entrypoint():
    cli()


if __name__ == "__main__":
    cli_entrypoint()
