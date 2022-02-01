import click

from koapy.backend.kiwoom_open_api_plus.core.tools.generate_python_stubs import (
    generate_python_stubs,
)
from koapy.config import default_encoding

default_dispatch_class_name = "KiwoomOpenApiPlusDispatchFunctionsGenerated"
default_dispatch_file_path = default_dispatch_class_name + ".py"

default_event_class_name = "KiwoomOpenApiPlusEventFunctionsGenerated"
default_event_file_path = default_event_class_name + ".py"


@click.command(
    short_help="Generate python stubs for OpenAPI Dispatch and Event.",
)
@click.option(
    "--dispatch-class-name",
    metavar="NAME",
    help="Name for class with Dispatch functions.",
    default=default_dispatch_class_name,
    show_default=True,
)
@click.option(
    "--dispatch-file-path",
    type=click.Path(),
    help="Path for python-stub with Dispatch functions.",
    default=default_dispatch_file_path,
    show_default=True,
)
@click.option(
    "--event-class-name",
    metavar="NAME",
    help="Name for class with Event functions.",
    default=default_event_class_name,
    show_default=True,
)
@click.option(
    "--event-file-path",
    type=click.Path(),
    help="Path for python-stub with Event functions.",
    default=default_event_file_path,
    show_default=True,
)
@click.option(
    "--encoding",
    metavar="ENCODING",
    help="Encoding for stub files.",
    default=default_encoding,
    show_default=True,
)
@click.option(
    "--force-overwrite",
    help="Force overwrite even if target file already exists.",
    is_flag=True,
    show_default=True,
)
def python_stubs(
    dispatch_class_name,
    dispatch_file_path,
    event_class_name,
    event_file_path,
    encoding,
    force_overwrite,
):
    generate_python_stubs(
        dispatch_class_name=dispatch_class_name,
        dispatch_file_path=dispatch_file_path,
        event_class_name=event_class_name,
        event_file_path=event_file_path,
        encoding=encoding,
        force_overwrite=force_overwrite,
    )
