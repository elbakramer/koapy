import click

from koapy.cli.extensions.functools import update_wrapper_with_click_params
from koapy.cli.extensions.parser import ClickArgumentParser
from koapy.cli.utils.verbose_option import full_verbose_option
from koapy.config import config

# grpc configs for default values
grpc_config = config.get("koapy.backend.kiwoom_open_api_plus.grpc")

default_server_bind_address = (
    grpc_config.get("server.bind_address")
    or grpc_config.get("server.host")
    or grpc_config.get("host")
)
default_server_host = default_server_bind_address
default_server_port = grpc_config.get("server.port") or grpc_config.get("port")

default_client_host = grpc_config.get("client.host") or grpc_config.get("host")
default_client_port = grpc_config.get("client.port") or grpc_config.get("port")

default_common_host = grpc_config.get("host") or grpc_config.get("client.host")
default_common_port = (
    grpc_config.get("port")
    or grpc_config.get("server.port")
    or grpc_config.get("client.port")
)


# server specific options
server_bind_address_option = click.option(
    "--bind-address",
    "--host",
    metavar="ADDRESS",
    help="Host address of gRPC server to bind.",
    default=default_server_bind_address,
    show_default=True,
)
server_port_option = click.option(
    "--port",
    metavar="PORT",
    type=int,
    help="Port number of gRPC server to bind.",
    default=default_server_port,
    show_default=True,
)
server_key_file_option = click.option(
    "--key-file",
    type=click.Path(),
    help="PEM encoded private key file for server SSL/TLS.",
)
server_cert_file_option = click.option(
    "--cert-file",
    type=click.Path(),
    help="PEM encoded certificate chain file for server SSL/TLS.",
)
server_root_certs_file_option = click.option(
    "--root-certs-file",
    type=click.Path(),
    help="""
    PEM encoded client root certificates file for client authentication.
    Assumes --require-client-auth flag is set if this option is given,
    unless --no-require-client-auth flag is set explicitly.
    """,
)
server_require_client_auth_option = click.option(
    "--require-client-auth",
    help="Require clients to be authenticated, root certificates are required.",
    is_flag=True,
)
server_no_require_client_auth_option = click.option(
    "--no-require-client-auth",
    help="Force not to require clients to be authenticated, even if root certificates are given.",
    is_flag=True,
)

server_options = [
    server_bind_address_option,
    server_port_option,
    server_key_file_option,
    server_cert_file_option,
    server_root_certs_file_option,
    server_require_client_auth_option,
    server_no_require_client_auth_option,
]


# client specific options
client_host_option = click.option(
    "--host",
    metavar="ADDRESS",
    help="Host address of gRPC server to connect.",
    default=default_client_host,
    show_default=True,
)
client_port_option = click.option(
    "--port",
    metavar="PORT",
    type=int,
    help="Port number of gRPC server to connect.",
    default=default_client_port,
    show_default=True,
)
client_enable_ssl_option = click.option(
    "--enable-ssl",
    help="""
    Enable SSL/TLS for gRPC connection.
    If --root-certs-file option is not given,
    will retrieve them from a default location chosen by gRPC runtime.
    """,
    is_flag=True,
)
client_root_certs_file_option = click.option(
    "--root-certs-file",
    type=click.Path(),
    help="PEM encoded root certificates file for SSL/TLS.",
)
client_key_file_option = click.option(
    "--key-file",
    type=click.Path(),
    help="PEM encoded private key file for client authentication.",
)
client_cert_file_option = click.option(
    "--cert-file",
    type=click.Path(),
    help="PEM encoded certificate chain file for client authentication.",
)

client_options = [
    client_host_option,
    client_port_option,
    client_enable_ssl_option,
    client_root_certs_file_option,
    client_key_file_option,
    client_cert_file_option,
]


# server and client options (resolving option conflicts)
server_and_client_bind_address_option = click.option(
    "--bind-address",
    "--server-host",
    metavar="ADDRESS",
    help="Host address of gRPC server to bind.",
    default=default_server_bind_address,
    show_default=True,
)
server_and_client_host_option = click.option(
    "--host",
    "--client-host",
    metavar="ADDRESS",
    help="Host address of gRPC server to connect.",
    default=default_client_host,
    show_default=True,
)
server_and_client_port_option = click.option(
    "--port",
    metavar="PORT",
    type=int,
    help="Port number of gRPC server to bind and connect.",
    default=default_common_port,
    show_default=True,
)
server_and_client_enable_ssl_option = click.option(
    "--enable-ssl",
    help="""
    Enable SSL/TLS for gRPC connection.
    If --client-root-certs-file option is not given,
    will retrieve them from a default location chosen by gRPC runtime.
    """,
    is_flag=True,
    show_default=True,
)
server_and_client_server_key_file_option = click.option(
    "--server-key-file",
    type=click.Path(),
    help="PEM encoded private key file for server SSL/TLS.",
)
server_and_client_server_cert_file_option = click.option(
    "--server-cert-file",
    type=click.Path(),
    help="PEM encoded certificate chain file for server SSL/TLS.",
)
server_and_client_server_root_certs_file_option = click.option(
    "--server-root-certs-file",
    type=click.Path(),
    help="""
    PEM encoded client root certificates file for client authentication.
    Assumes --require-client-auth flag is set if this option is given,
    unless --no-require-client-auth flag is set explicitly.
    """,
)
server_and_client_require_client_auth_option = click.option(
    "--require-client-auth",
    help="Require clients to be authenticated, root certificates are required.",
    is_flag=True,
)
server_and_client_no_require_client_auth_option = click.option(
    "--no-require-client-auth",
    help="Foce not to require clients to be authenticated, even if root certificates are given.",
    is_flag=True,
)
server_and_client_client_root_certs_file_option = click.option(
    "--client-root-certs-file",
    type=click.Path(),
    help="PEM encoded root certificates file for SSL/TLS.",
)
server_and_client_client_key_file_option = click.option(
    "--client-key-file",
    type=click.Path(),
    help="PEM encoded private key file for client authentication.",
)
server_and_client_client_cert_file_option = click.option(
    "--client-cert-file",
    type=click.Path(),
    help="PEM encoded certificate chain file for client authentication.",
)

server_and_client_options = [
    server_and_client_bind_address_option,
    server_and_client_host_option,
    server_and_client_port_option,
    server_and_client_enable_ssl_option,
    server_and_client_server_key_file_option,
    server_and_client_server_cert_file_option,
    server_and_client_server_root_certs_file_option,
    server_and_client_require_client_auth_option,
    server_and_client_no_require_client_auth_option,
    server_and_client_client_root_certs_file_option,
    server_and_client_client_key_file_option,
    server_and_client_client_cert_file_option,
]


def grpc_server_options():
    def decorator(f):
        @click.pass_context
        @server_bind_address_option
        @server_port_option
        @server_key_file_option
        @server_cert_file_option
        @server_root_certs_file_option
        @server_require_client_auth_option
        @server_no_require_client_auth_option
        def new_func(ctx: click.Context, *args, **kwargs):
            key_file = kwargs.get("key_file")
            cert_file = kwargs.get("cert_file")
            root_certs_file = kwargs.get("root_certs_file")
            require_client_auth = kwargs.get("require_client_auth")
            no_require_client_auth = kwargs.pop("no_require_client_auth")

            # both --key-file and --cert-file should be given
            if bool(key_file) != bool(cert_file):
                ctx.fail("both --key-file and --cert-file should be given.")

            # assume --require-client-auth flag is set if --root-certs-file is given
            if root_certs_file is not None:
                require_client_auth = True
                kwargs["require_client_auth"] = require_client_auth

            # value of --require-client-auth flag should be false if --no-require-client-auth flag is set
            if no_require_client_auth:
                require_client_auth = False
                kwargs["require_client_auth"] = require_client_auth

            # --require-client-auth flag is set but no --root-certs-file was given
            if require_client_auth and root_certs_file is None:
                ctx.fail(
                    "--require-client-auth flag is set but no --root-certs-file was  given."
                )

            return ctx.invoke(f, *args, **kwargs)

        return update_wrapper_with_click_params(new_func, f)

    return decorator


def grpc_client_options():
    def decorator(f):
        @click.pass_context
        @client_host_option
        @client_port_option
        @client_enable_ssl_option
        @client_root_certs_file_option
        @client_key_file_option
        @client_cert_file_option
        def new_func(ctx: click.Context, *args, **kwargs):
            enable_ssl = kwargs.get("enable_ssl")
            root_certs_file = kwargs.get("root_certs_file")
            key_file = kwargs.get("key_file")
            cert_file = kwargs.get("cert_file")

            # assume --enable-ssl flag is set if --root-certs-file is given
            if root_certs_file is not None:
                enable_ssl = True
                kwargs["enable_ssl"] = enable_ssl

            # both --key-file and --cert-file should be given
            if bool(key_file) != bool(cert_file):
                ctx.fail("both --key-file and --cert-file should be given.")

            return ctx.invoke(f, *args, **kwargs)

        return update_wrapper_with_click_params(new_func, f)

    return decorator


def grpc_server_and_client_options():
    def decorator(f):
        @click.pass_context
        @server_and_client_bind_address_option
        @server_and_client_host_option
        @server_and_client_port_option
        @server_and_client_enable_ssl_option
        @server_and_client_server_key_file_option
        @server_and_client_server_cert_file_option
        @server_and_client_server_root_certs_file_option
        @server_and_client_require_client_auth_option
        @server_and_client_no_require_client_auth_option
        @server_and_client_client_root_certs_file_option
        @server_and_client_client_key_file_option
        @server_and_client_client_cert_file_option
        def new_func(ctx: click.Context, *args, **kwargs):
            # server related options and logics
            key_file = kwargs.get("server_key_file")
            cert_file = kwargs.get("server_cert_file")
            root_certs_file = kwargs.get("server_root_certs_file")
            require_client_auth = kwargs.get("require_client_auth")
            no_require_client_auth = kwargs.pop("no_require_client_auth")

            # both --key-file and --cert-file should be given
            if bool(key_file) != bool(cert_file):
                ctx.fail(
                    "both --server-key-file and --server-cert-file should be given."
                )

            # assume --require-client-auth flag is set if --root-certs-file is given
            if root_certs_file is not None:
                require_client_auth = True
                kwargs["require_client_auth"] = require_client_auth

            # value of --require-client-auth flag should be false if --no-require-client-auth flag is set
            if no_require_client_auth:
                require_client_auth = False
                kwargs["require_client_auth"] = require_client_auth

            # --require-client-auth flag is set but no --root-certs-file was given
            if require_client_auth and root_certs_file is None:
                ctx.fail(
                    "--require-client-auth flag is set but no --server-root-certs-file was  given."
                )

            # client related options and logics
            enable_ssl = kwargs.get("enable_ssl")
            root_certs_file = kwargs.get("client_root_certs_file")
            key_file = kwargs.get("client_key_file")
            cert_file = kwargs.get("client_cert_file")

            # assume --enable-ssl flag is set if --root-certs-file is given
            if root_certs_file is not None:
                enable_ssl = True
                kwargs["enable_ssl"] = enable_ssl

            # both --key-file and --cert-file should be given
            if bool(key_file) != bool(cert_file):
                ctx.fail(
                    "both --client-key-file and --client-cert-file should be given."
                )

            return ctx.invoke(f, *args, **kwargs)

        return update_wrapper_with_click_params(new_func, f)

    return decorator


server_argument_parser = ClickArgumentParser(server_options + [full_verbose_option()])
client_argument_parser = ClickArgumentParser(client_options + [full_verbose_option()])

server_and_client_argument_parser = ClickArgumentParser(
    server_and_client_options + [full_verbose_option()]
)
