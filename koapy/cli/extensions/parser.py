import sys

from argparse import Namespace
from typing import Any, Callable, List, Optional, Sequence, Tuple, TypeVar, Union

import click

from click import Command

Function = TypeVar("Function", bound=Callable[..., Any])
FunctionOrCommand = TypeVar(
    "FunctionOrCommand", bound=Union[Callable[..., Any], Command]
)

ArgumentDecorator = Callable[[FunctionOrCommand], FunctionOrCommand]
CommandDecorator = Callable[[Function], Command]


class ArgumentParser:
    def parse_args(
        self,
        args: Optional[Sequence[str]] = None,
        namespace: Optional[Namespace] = None,
    ) -> Namespace:
        raise NotImplementedError

    def parse_known_args(
        self,
        args: Optional[Sequence[str]] = None,
        namespace: Optional[Namespace] = None,
    ) -> Tuple[Namespace, List[str]]:
        raise NotImplementedError


class ClickArgumentParser(ArgumentParser):

    _unrecognized_args_attr = "args"

    def __init__(
        self,
        params: Sequence[ArgumentDecorator],
        command: Optional[CommandDecorator] = None,
        help_option_names: Optional[Sequence[str]] = None,
    ):
        if help_option_names is None:
            help_option_names = ["-h", "--help"]

        if command is None:
            command = click.command(
                context_settings=dict(help_option_names=help_option_names)
            )

        self._params = params
        self._command = command
        self._help_option_names = help_option_names

    def _callback(self, *args, **kwargs):
        return args, kwargs

    def _parse_args(
        self,
        args: Optional[Sequence[str]] = None,
        namespace: Optional[Namespace] = None,
        ignore_unknown_options: bool = False,
        allow_extra_args: bool = False,
        allow_interspersed_args: bool = True,
    ) -> Tuple[Namespace, List[str]]:

        if args is None:
            args = sys.argv[1:]
        else:
            args = list(args)

        if namespace is None:
            namespace = Namespace()

        def callback(*args, **kwargs):
            return self._callback(*args, **kwargs)

        if ignore_unknown_options:
            unrecognized_args_param = click.argument(
                self._unrecognized_args_attr,
                nargs=-1,
                type=click.UNPROCESSED,
                metavar="[ARGS]...",
            )
            callback = unrecognized_args_param(callback)

        for decorator in reversed(self._params):
            callback = decorator(callback)

        command = self._command(callback)
        context_settings = dict(
            help_option_names=self._help_option_names,
            ignore_unknown_options=ignore_unknown_options,
            allow_extra_args=allow_extra_args,
            allow_interspersed_args=allow_interspersed_args,
        )
        command.context_settings.update(context_settings)

        ret = command.main(args, standalone_mode=False)

        if isinstance(ret, int):
            sys.exit(ret)

        callback_args, callback_kwargs = ret

        assert len(callback_args) == 0

        for key, value in callback_kwargs.items():
            setattr(namespace, key, value)

        unrecognized_args = []

        if hasattr(namespace, self._unrecognized_args_attr):
            unrecognized_args = getattr(namespace, self._unrecognized_args_attr)
            unrecognized_args = list(unrecognized_args)
            delattr(namespace, self._unrecognized_args_attr)

        return namespace, unrecognized_args

    def parse_args(
        self,
        args: Optional[Sequence[str]] = None,
        namespace: Optional[Namespace] = None,
    ) -> Namespace:
        namespace, _unrecognized_args = self._parse_args(args, namespace)
        return namespace

    def parse_known_args(
        self,
        args: Optional[Sequence[str]] = None,
        namespace: Optional[Namespace] = None,
    ) -> Tuple[Namespace, List[str]]:
        namespace, unrecognized_args = self._parse_args(
            args,
            namespace,
            ignore_unknown_options=True,
        )
        return namespace, unrecognized_args
