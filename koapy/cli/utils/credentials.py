import os

import click

from koapy.config import (
    config,
    config_from_dict,
    default_user_config_filepath,
    save_config,
    user_config,
)


def prompt_credentials():
    credentials = config.get("koapy.backend.kiwoom_open_api_plus.credentials")

    default_user_id = credentials["user_id"]
    default_user_password = credentials["user_password"]
    default_server = "simulation" if credentials["is_simulation"] else "real"
    default_cert_password = credentials["cert_password"]

    user_id = click.prompt("User ID", default=default_user_id)
    user_password = click.prompt(
        "User Password",
        hide_input=True,
        default=default_user_password,
        show_default=False,
    )
    is_simulation = (
        click.prompt(
            "Server Type",
            type=click.Choice(["real", "simulation"], case_sensitive=False),
            default=default_server,
        )
        == "simulation"
    )
    if is_simulation:
        cert_password = default_cert_password
    else:
        cert_password = click.prompt(
            "Cert Password",
            hide_input=True,
            default=default_cert_password,
            show_default=False,
        )

    account_passwords = {}
    if is_simulation:
        account_passwords["0000000000"] = "0000"
    else:
        account_count = click.prompt("Account Count", type=int, default=1)
        for _ in range(account_count):
            account_number = click.prompt("Account Number", default="0000000000")
            account_password = click.prompt(
                "Account Password",
                hide_input=True,
                show_default=False,
            )
            account_passwords[account_number] = account_password

    credentials = {
        "user_id": user_id,
        "user_password": user_password,
        "cert_password": cert_password,
        "is_simulation": is_simulation,
        "account_passwords": account_passwords,
    }
    credentials = config_from_dict(credentials)

    return credentials


def get_credentials(interactive=False):
    if not interactive:
        credentials = config.get("koapy.backend.kiwoom_open_api_plus.credentials")
    else:
        credentials = prompt_credentials()
        save_credentials = (
            click.prompt(
                "Save credentials info into a config file?",
                type=click.Choice(["y", "n"], case_sensitive=False),
                default="n",
            )
            == "y"
        )
        if save_credentials:
            config_path = click.prompt(
                "Path to save config file", default=default_user_config_filepath
            )

            if os.path.exists(config_path):
                should_write = (
                    click.prompt(
                        "The file already exists, overwrite?",
                        type=click.Choice(["y", "n"], case_sensitive=False),
                        default="n",
                    )
                    == "y"
                )
            else:
                should_write = True

            if should_write:
                user_config.put(
                    "koapy.backend.kiwoom_open_api_plus.credentials", credentials
                )
                save_config(config_path, user_config)

    return credentials
