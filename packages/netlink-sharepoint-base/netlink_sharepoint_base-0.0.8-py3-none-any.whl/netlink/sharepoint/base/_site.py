from copy import deepcopy
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential

from netlink.logging import logger


class Site:
    _url = ""
    _client_id = ""
    _client_secret = ""

    def __init__(self, url: str = None, client_id: str = None, client_secret: str = None, **kwargs) -> None:
        self._context = ClientContext(url or self._url).with_credentials(
            ClientCredential(client_id=client_id or self._client_id, client_secret=client_secret or self._client_secret)
        )
        logger.debug(f"Initialized connection Sharepoint as {self.url}")
        self._users = None
        self._lists = {}

    def get_list(self, name: str):
        if name not in self._lists:
            self._lists[name] = self._context.web.lists.get_by_title(name)
        return self._lists[name]

    @property
    def url(self):
        return self._context.base_url

    def get_lists(self, hidden: bool = False):
        if hidden:
            selector = lambda x: True
        else:
            selector = lambda x: x.properties["BaseTemplate"] == 100 and x.title not in ("TaxonomyHiddenList",)
        return [i for i in self._context.lists.get().execute_query() if selector(i)]

    def get_list_items(self, name):
        return self.get_list(name).items.get().execute_query()

    def commit(self):
        self._context.execute_batch()

    def get_list_columns(self, name, hidden=False):
        if not isinstance(name, str):
            name = name.title
        if hidden:
            selector = lambda x: True
        else:
            selector = (
                lambda x: not x.hidden
                and x.group not in ("_Hidden",)
                and not x.internal_name.startswith("_")
                and x.internal_name
                not in (
                    "Edit",
                    "LinkTitleNoMenu",
                    "LinkTitle",
                    "DocIcon",
                    "ItemChildCount",
                    "FolderChildCount",
                    "AppAuthor",
                    "AppEditor",
                    "ComplianceAssetId",
                    "Modified",
                    "Created",
                    "Author",
                    "Editor",
                    "Attachments",
                )
            )
        return [i for i in self.get_list(name).fields.get().execute_query() if selector(i)]

    @property
    def users(self):
        if self._users is None:
            self._users = {}
            for i in self._context.web.site_users.get().execute_query():
                if i.principal_type == 1 and i.user_principal_name is not None:
                    email = i.get_property("Email").lower()
                    name = i.title.split("(")[0].strip()
                    if ", " in name:
                        family_name, given_name = name.split(", ")
                    elif ". " in name:
                        given_name, family_name = name.split(".")
                    else:
                        logger.warning(f"Cannot determine Given and Family Name for '{name}' <{email}>")
                        family_name, given_name = name, ''
                    given_name = given_name.capitalize()
                    family_name = family_name.capitalize()
                    name = f"{family_name}, {given_name}"
                    self._users[i.id] = {
                        "name": name,
                        "family_name": family_name,
                        "given_name": given_name,
                        "email": email,
                    }
        return deepcopy(self._users)
