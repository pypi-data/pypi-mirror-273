from __future__ import annotations

import json
from dataclasses import asdict
from typing import TYPE_CHECKING

from kaas_cli import __version__

import click
from dacite import from_dict, Config

from .client import KaasClient
from .config import DEFAULT_DIRECTORY, DEFAULT_PROJECT_ID, DEFAULT_TOKEN, SERVER_URL, CustomHelpOption

if TYPE_CHECKING:
    from click.core import Context

from .types import Vault, Key


@click.group()
@click.option("--url", "-u", default=SERVER_URL, show_default=True, help="Server URL")
@click.option("--token", "-t", default=DEFAULT_TOKEN, help="Personal access key for vault")
@click.option("--vault", "-v", default=DEFAULT_PROJECT_ID, help="Vault ID")
@click.version_option(version=__version__, prog_name='kaas-cli')
@click.pass_context
def cli(ctx: Context, url: str, token: str | None, vault: str | None) -> None:
    """KaaS Command Line Interface"""
    ctx.ensure_object(dict)
    ctx.obj["client"] = KaasClient(url=url, token=token, vault=vault)


@cli.command(cls=CustomHelpOption, help="Upload proofs to the remote server.")
@click.option(
    "-d",
    "--directory",
    default=DEFAULT_DIRECTORY,
    show_default=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Directory containing proofs to upload",
)
@click.option("--url", "-u", default=SERVER_URL, show_default=True, help="Server URL")
@click.option("--token", "-t", default=DEFAULT_TOKEN, help="Personal access key for vault")
@click.option("--vault", "-v", default=DEFAULT_PROJECT_ID, help="Vault ID")
@click.pass_context
def upload(ctx: Context, directory: str, url: str | None, token: str | None, vault: str | None) -> None:
    ctx.ensure_object(dict)
    client: KaasClient = KaasClient(url=url, token=token, vault=vault)
    ctx.obj["client"] = client
    response_message = client.upload_files_s3(directory=directory)
    click.echo(response_message)


@cli.command(cls=CustomHelpOption, help="Download proofs from the remote server.")
@click.option(
    "-d",
    "--directory",
    default=DEFAULT_DIRECTORY,
    show_default=True,
    type=click.Path(exists=False, file_okay=False, dir_okay=True),
    help="Directory to save downloaded proofs",
)
@click.option("--url", "-u", default=SERVER_URL, show_default=True, help="Server URL")
@click.option("--token", "-t", default=DEFAULT_TOKEN, help="Personal access key for vault")
@click.option("--vault", "-v", default=DEFAULT_PROJECT_ID, help="Vault ID")
@click.argument("version_address", required=False)
@click.pass_context
def download(
        ctx: Context,
        version_address: str | None,
        directory: str, url: str | None, token: str | None, vault: str | None
) -> None:  # type: ignore
    ctx.ensure_object(dict)
    client: KaasClient = KaasClient(url=url, token=token, vault=vault)
    ctx.obj["client"] = client
    if not version_address:
        message = client.download_last_version(target_directory=directory)
        if message:
            click.echo(message)
        return

    message = client.download_version(version_address, target_directory=directory)
    if message:
        click.echo(message)


@cli.command(cls=CustomHelpOption, help="Say hello.")
@click.option("-n", "--name", default="World", show_default=True, help="Name to say hello to")
@click.pass_context
def hello(ctx: Context, name: str) -> None:
    client: KaasClient = ctx.obj["client"]

    response = client.hello(name=name)
    click.echo(response)


@cli.command(cls=CustomHelpOption, help="Login to the system.")
@click.pass_context
def login(ctx: Context) -> None:
    client: KaasClient = ctx.obj["client"]
    data = client.login()
    click.echo(f"Your user code: {data.user_code}")
    click.echo(f"Open the link and type your code {data.verification_uri}")
    click.echo("Then hit 'enter'")
    input_value = click.prompt("Press Enter to continue or type 'q' to quit", default="", show_default=False)
    if input_value.lower() == 'q':
        click.echo("You left authentication")
        return
    click.echo("You pressed Enter. The application continues...")
    confirm_success = client.confirm_login(data.device_code).success
    if not confirm_success:
        click.echo("Authentication failed")
        return
    click.echo("Access token received. We store it in cache folder")


@cli.command(cls=CustomHelpOption, help="List local proofs.", aliases=['l', 'ls'])
@click.option(
    "-d",
    "--directory",
    default=DEFAULT_DIRECTORY,
    show_default=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Directory to list local proofs",
)
@click.option("--remote", is_flag=True, help="List remote proofs instead of local proofs", default=False)
@click.pass_context
def list(ctx: Context, directory: str = DEFAULT_DIRECTORY, remote: bool = False) -> None:
    client: KaasClient = ctx.obj["client"]
    if remote:
        proofs = client.list_remote()
    else:
        proofs = client.list_local_proofs(directory=directory)
    if not proofs:
        click.echo('No proofs found')
    for proof in proofs:
        click.echo(proof)


def list_remote(ctx: Context) -> None:
    client: KaasClient = ctx.obj["client"]
    proofs = client.list_remote()
    for proof in proofs:
        click.echo(proof)


@cli.command(cls=CustomHelpOption, name="check-auth", help="Check authentication status.")
@click.pass_context
def check_auth(ctx: Context) -> None:
    client: KaasClient = ctx.obj["client"]
    is_authenticated = client.check()
    if is_authenticated:
        click.echo("You are currently authenticated.")
    else:
        click.echo("You are not authenticated. Please log in.")


@cli.command(cls=CustomHelpOption, name="list-vaults", help="List remote vaults owned by your KaaS account.")
@click.pass_context
def list_vaults(ctx: Context) -> None:
    client: KaasClient = ctx.obj["client"]
    vaults = client.list_vaults()

    if not vaults:
        click.echo("No vaults")
        return

    vaults = [from_dict(data_class=Vault, data=item, config=Config(cast=[Vault])) for item in vaults]

    filtered_data = [asdict(vault) for vault in vaults]
    formatted_json = json.dumps(filtered_data, indent=4)
    click.echo(f"Vaults:\n{formatted_json}")


@cli.command(cls=CustomHelpOption, name="list-keys", help="List remote keys owned by <VAULT_ADDRESS>")
@click.argument("vault_address", required=True)
@click.pass_context
def list_keys(ctx: Context, vault_address: str) -> None:
    client: KaasClient = ctx.obj["client"]
    keys = client.list_keys(vault_address)

    if not keys:
        click.echo(f"No keys found for vault {vault_address}")
        return

    keys = [from_dict(data_class=Key, data=item, config=Config(cast=[Key])) for item in keys]
    filtered_data = [asdict(key) for key in keys]
    formatted_json = json.dumps(filtered_data, indent=4)
    click.echo(f"Keys for vault {vault_address}:\n{formatted_json}")


@cli.command(cls=CustomHelpOption, name="list-versions",
             help="List remote versions of a cached artifact, with <VAULT_ADDRESS> as the address of the vault.")
@click.argument("vault_address", required=True)
@click.pass_context
def list_versions(ctx: Context, vault_address: str) -> None:
    client: KaasClient = ctx.obj["client"]
    versions = client.list_versions(vault_address)

    if not versions:
        click.echo(f"No versions found for vault {vault_address}")
        return

    click.echo(f"Versions for vault {vault_address}:")
    formatted_json = json.dumps(versions, indent=4)
    click.echo(formatted_json)


@cli.command(cls=CustomHelpOption, name="logout", help="Log out from the system.")
@click.pass_context
def logout(ctx: Context) -> None:
    client: KaasClient = ctx.obj["client"]
    logout_success = client.logout()
    if logout_success:
        click.echo("You have been logged out successfully.")
    else:
        click.echo("Logout failed. You may not be logged in.")
