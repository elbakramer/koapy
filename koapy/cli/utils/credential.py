import os

import click

from koapy.config import (
    config,
    config_from_dict,
    default_user_config_path,
    save_config,
    user_config,
)


def prompt_credential():
    credential = config.get("koapy.backend.kiwoom_open_api_plus.credential")

    default_user_id = credential["user_id"]
    default_user_password = credential["user_password"]
    default_server = "simulation" if credential["is_simulation"] else "real"
    default_cert_password = credential["cert_password"]

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
    account_count = click.prompt("Account Count", type=int, default=1)
    account_passwords = {}
    for _ in range(account_count):
        account_number = click.prompt("Account Number", default="0000000000")
        account_password = click.prompt(
            "Account Password",
            hide_input=True,
            default="0000",
            show_default=False,
        )
        account_passwords[account_number] = account_password

    credential = {
        "user_id": user_id,
        "user_password": user_password,
        "cert_password": cert_password,
        "is_simulation": is_simulation,
        "account_passwords": account_passwords,
    }
    credential = config_from_dict(credential)

    return credential


def get_credential(interactive=False):
    if not interactive:
        credential = config.get("koapy.backend.kiwoom_open_api_plus.credential")
    else:
        credential = prompt_credential()
        save_credential = (
            click.prompt(
                "Save credential info into a config file?",
                type=click.Choice(["y", "n"], case_sensitive=False),
                default="n",
            )
            == "y"
        )
        if save_credential:
            config_path = click.prompt(
                "Path to save config file", default=default_user_config_path
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
                    "koapy.backend.kiwoom_open_api_plus.credential", credential
                )
                save_config(config_path, user_config)

    return credential
