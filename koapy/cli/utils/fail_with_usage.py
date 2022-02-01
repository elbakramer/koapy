import click


def get_help(ctx):
    return ctx.get_help()


def get_help_without_usage(ctx):
    formatter = ctx.make_formatter()
    command = ctx.command
    command.format_help_text(ctx, formatter)
    command.format_options(ctx, formatter)
    command.format_epilog(ctx, formatter)
    help_without_usage = formatter.getvalue().rstrip("\n")
    return help_without_usage


def fail_with_usage(message=None, ctx=None):
    if ctx is None:
        ctx = click.get_current_context()
    if message is not None:
        click.UsageError(message, ctx).show()
        click.echo()
        click.echo(get_help_without_usage(ctx))
    else:
        click.echo(get_help(ctx))
    ctx.exit(click.UsageError.exit_code)
