import pathlib

import click
import toml as toml_

from ._site import Site

from netlink.logging import logger

logger.set_level(logger.WARNING)


@click.command()
@click.option("-u", "--url", help="Sharepoint URL")
@click.option("-i", "--client-id", help="Client ID")
@click.option("-s", "--client-secret", help="Client Secret")
@click.option(
    "-t",
    "--toml",
    type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path),
    help="TOML file with 'url', 'client_id', and 'client_secret'",
)
@click.option("-f", "--fields", is_flag=True, help="include fields")
@click.option("--hidden", is_flag=True, help="include hidden lists (and fields)")
@click.argument("name", nargs=-1)
def print_list_info(name, url, client_id, client_secret, toml, fields, hidden):
    """Print information about SharePoint List(s)

    If NAME is not provided, all lists are returned.

    """
    if toml is not None:
        with toml.open("r", encoding="utf-8-sig") as f:
            d = toml_.load(f)
        url, client_id, client_secret = d["url"], d["client_id"], d["client_secret"]
    if url is None or client_id is None or client_secret is None:
        raise click.UsageError(
            "Essential options missing. Either provide 'url', 'client_id', and 'client_secret', or a respective 'toml'-file."
        )
    site = Site(url=url, client_id=client_id, client_secret=client_secret)
    for i in site.get_lists(hidden=hidden):
        if name:
            if i.title not in name:
                continue
        print(i.title)
        if fields:
            for j in site.get_list_columns(name=i.title, hidden=hidden):
                print(
                    f"    {j.title:25}  {j.type_as_string:10}  {j.internal_name}{'Id' if j.type_as_string in ('User', 'Lookup') else ''}"
                )
            print()
