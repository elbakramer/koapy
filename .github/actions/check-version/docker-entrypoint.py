#!/usr/bin/env python

import json

import click

from actions_toolkit import core


class BooleanOption(click.Option):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = click.Choice(["true", "false", ""], case_sensitive=False)
        self.callback = self._callback
        self._option_parser = None
        self._option_parser__match_long_opt = None
        self._option = None
        self._option_process = None

    def _callback(self, ctx, param, value):
        if value and isinstance(value, str):
            value = json.loads(value.lower())
        return value

    def _get_value_from_state(self, opt, option, state):
        if state.rargs and not any(
            state.rargs[0].startswith(prefix) for prefix in self._option.prefixes
        ):
            return state.rargs.pop(0)

    def _match_long_opt(self, opt, explicit_value, state):
        try:
            self._option_parser__match_long_opt(opt, explicit_value, state)
        except click.BadOptionUsage:
            option = self._option_parser._long_opt.get(opt)
            if not option:
                return
            if explicit_value is not None:
                value = explicit_value
            else:
                value = self._get_value_from_state(opt, option, state)
            option.process(value, state)

    def _process(self, value, state):
        if value is None:
            value = True
        elif not value:
            value = None
        state.opts[self._option.dest] = value
        state.order.append(self._option.obj)

    def add_to_parser(self, parser, ctx):
        self._option_parser = parser
        self._option_parser__match_long_opt = parser._match_long_opt
        parser._match_long_opt = self._match_long_opt
        super().add_to_parser(parser, ctx)
        for name in self.opts:
            option = parser._long_opt.get(name) or parser._short_opt.get(name)
            if option:
                self._option = option
                self._option_process = option.process
                option.process = self._process
                break


@click.command()
@click.argument("vcs", default=core.get_input("vcs", required=False) or "any")
@click.option(
    "--metadata", cls=BooleanOption, default=core.get_input("metadata", required=False)
)
@click.option(
    "--no-metadata",
    cls=BooleanOption,
    default=core.get_input("no_metadata", required=False),
)
@click.option(
    "--dirty", cls=BooleanOption, default=core.get_input("dirty", required=False)
)
@click.option(
    "--tagged-metadata",
    cls=BooleanOption,
    default=core.get_input("tagged_metadata", required=False),
)
@click.option("--pattern", default=core.get_input("pattern", required=False))
@click.option("--format", default=core.get_input("format", required=False))
@click.option("--style", default=core.get_input("style", required=False))
@click.option(
    "--latest-tag",
    cls=BooleanOption,
    default=core.get_input("latest_tag", required=False),
)
@click.option(
    "--bump", cls=BooleanOption, default=core.get_input("bump", required=False)
)
@click.option("--tag-dir", default=core.get_input("tag_dir", required=False))
@click.option(
    "--is-postrelease",
    cls=BooleanOption,
    default=core.get_input("is_postrelease", required=False),
)
def cli(
    vcs,
    metadata,
    no_metadata,
    dirty,
    tagged_metadata,
    pattern,
    format,
    style,
    latest_tag,
    bump,
    tag_dir,
    is_postrelease,
):
    import inspect

    from dunamai import Vcs, Version
    from packaging.version import parse

    core.start_group("Check dynamic version using `dunamai`")
    kwargs = {}
    if pattern:
        kwargs["pattern"] = pattern
    if latest_tag:
        kwargs["latest_tag"] = True
    if tag_dir:
        kwargs["tag_dir"] = tag_dir
    print(
        ">>> dunamai_version = Version.from_vcs(Vcs(%r)%s)"
        % (
            vcs,
            ", "
            + ", ".join(["{}={!r}".format(key, value) for key, value in kwargs.items()])
            if len(kwargs)
            else "",
        )
    )
    dunamai_version = Version.from_vcs(Vcs(vcs), **kwargs)
    print("Checked version: %s" % dunamai_version)
    core.end_group()

    core.start_group("Serialize dunamai version")
    kwargs = {}
    if metadata:
        kwargs["metadata"] = True
    if no_metadata:
        kwargs["metadata"] = False
    if dirty:
        kwargs["dirty"] = dirty
    if format:
        kwargs["format"] = format
    if style:
        kwargs["style"] = style
    if bump:
        kwargs["bump"] = bump
    if tagged_metadata:
        kwargs["tagged_metadata"] = tagged_metadata
    print(
        ">>> serialized_version = dunamai_version.serialize(%s)"
        % ", ".join(["{}={!r}".format(key, value) for key, value in kwargs.items()])
    )
    serialized_version = dunamai_version.serialize(**kwargs).replace(".dev0", "")
    print("Serialized version: %s" % serialized_version)
    core.end_group()

    core.start_group("Analyze the serialized version using `packaging.version.parse()`")
    packaging_version = parse(serialized_version)

    if packaging_version.is_postrelease and not is_postrelease:
        print(
            "Detected version is in postrelease format but prerelease format is desired"
        )
        print("Bumping version to be a prerelease format")
        kwargs["bump"] = True
        serialized_version = dunamai_version.serialize(**kwargs).replace(".dev0", "")
        print(
            ">>> serialized_version = dunamai_version.serialize(%s)"
            % ", ".join(["{}={!r}".format(key, value) for key, value in kwargs.items()])
        )
        print("Bumped version: %s" % serialized_version)
        packaging_version = parse(serialized_version)

    outputs = {}
    outputs["version"] = "%s" % packaging_version
    outputs["is_finalrelease"] = (
        not packaging_version.is_prerelease
        and not packaging_version.is_devrelease
        and not packaging_version.is_postrelease
    )
    attributes = [
        (attr, value)
        for attr, value in inspect.getmembers(packaging_version)
        if not attr.startswith("_")
    ]
    for attr, value in attributes:
        outputs[attr] = value
    core.end_group()

    core.start_group("Analyzed version attributes")
    for attr, value in outputs.items():
        print("{}: {}".format(attr, value))
    core.end_group()

    for attr, value in outputs.items():
        core.set_output(attr, value)


def main():
    cli()  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    main()
