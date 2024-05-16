from time import sleep

import validators
from rich import print
from rich.panel import Panel
from rich.progress import SpinnerColumn, Progress
from rich.prompt import Prompt, Confirm

from pcli import PerianTyper
from pcli import db
from pcli.colors import PERIAN_LIME, PERIAN_PURPLE_LIGHT
from pcli.commands.accelerator_type import accelerator_type_command
from pcli.commands.config import config_command
from pcli.commands.instance_type import instance_type_command
from pcli.commands.job import job_command
from pcli.commands.billing import billing_command
from pcli.util.setup import setup
from pcli.responses import (
    success,
    MAGNIFYING_GLASS_EMOJI_UNICODE,
    InvalidMailException,
    AbortedException,
    NoOrganizationException,
    handle_exception,
    ExceptionLevel,
    DefaultApiException,
    OrganizationValidationException,
    AuthenticationFailedException
)
from pcli.api.organization import get_organization

# setting up the cli
setup()

# creating custom main typer cli
pcli = PerianTyper(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="[bold "
    + PERIAN_LIME
    + " ]Perian Sky Platform CLI [/bold "
    + PERIAN_LIME
    + "]",
)

# adding complex commands to cli
pcli.add_typer(
    config_command, name="config", rich_help_panel="Configuration & Utilities"
)
pcli.add_typer(job_command, name="job")
pcli.add_typer(instance_type_command, name="instance-type")
pcli.add_typer(accelerator_type_command, name="accelerator-type")
pcli.add_typer(billing_command, name="billing", rich_help_panel="Account")


@pcli.command("login", rich_help_panel="Account")
@handle_exception(InvalidMailException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(AbortedException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(DefaultApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(OrganizationValidationException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(NoOrganizationException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(AuthenticationFailedException, exit=True, level=ExceptionLevel.WARNING)
def login():
    print(
        Panel.fit(
            "[bold "
            + PERIAN_PURPLE_LIGHT
            + "] Welcome to the Perian Sky Platform CLI [/bold "
            + PERIAN_PURPLE_LIGHT
            + "] \n\n"
            + MAGNIFYING_GLASS_EMOJI_UNICODE
            + "All login information can be found in your signup e-mail"
        )
    )
    organization_name = Prompt.ask("Organization name")
    contact_mail_address = Prompt.ask("Contact E-Mail Address")
    access_token = Prompt.ask("Access token")

    if not validators.email(contact_mail_address):
        raise InvalidMailException(
            f"The provided e-mail '[bold underline]{contact_mail_address}[/bold underline]' is invalid."
        )

    # getting stored organization data
    organization_data = db.get("organization")

    # warn user about override
    if organization_data:
        confirm_override = Confirm.ask(
            "An organization is already logged in and setting up a new one would override the data. Do you confirm?"
        )
        if not confirm_override:
            raise AbortedException()

    with Progress(
        SpinnerColumn(style=PERIAN_PURPLE_LIGHT),
        "Validating with Sky Platform",
        transient=True,
    ) as progress:
        progress.add_task(description="Validating with Sky Platform", total=None)

        # validating login information with backend
        perian_organization = get_organization({
            "name": organization_name,
            "token": access_token,
            "email": contact_mail_address,
        })

        valid_name = perian_organization['organization']['name'] == organization_name
        valid_mail = perian_organization['organization']['contact_email_address'] == contact_mail_address
        valid_token = perian_organization['organization']['access_token'] == access_token

        if not valid_name or not valid_mail or not valid_token:
            raise OrganizationValidationException()


    db.set(
        "organization",
        {
            "name": organization_name,
            "token": access_token,
            "email": contact_mail_address,
        },
    )
    success(f"Login successful.")


@pcli.command("logout", rich_help_panel="Account")
@handle_exception(NoOrganizationException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(AbortedException, exit=True, level=ExceptionLevel.WARNING)
def logout():
    # getting stored organization data
    organization_data = db.get("organization")

    if not organization_data:
        raise NoOrganizationException("No logged in organization could be found.")

    confirm_delete = Confirm.ask("Please confirm logout")

    if not confirm_delete:
        raise AbortedException()

    # deleting registry from db
    db.set("organization", None)
    success(f"Logout successful.")
