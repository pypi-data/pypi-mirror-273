# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['base']

package_data = \
{'': ['*']}

install_requires = \
['Office365-REST-Python-Client>=2.5.9',
 'click>=8.1.3',
 'netlink-logging>=0.1.15']

entry_points = \
{'console_scripts': ['sharepoint_list_info = '
                     'netlink.sharepoint.base.cli:print_list_info']}

setup_kwargs = {
    'name': 'netlink-sharepoint-base',
    'version': '0.0.8',
    'description': 'Basic Tools for interaction with Sharepoint Sites',
    'long_description': '# netlink-sharepoint-base\n\n## Basic Tools for interaction with Sharepoint Sites\n\nThis has been moved from `netlink-sharepoint`\n\nFor now only **Lists** are considered.\n\n## `sharepoint_list_info`\n\nScript to help mapping\n\n```shell\nUsage: sharepoint_list_info.py [OPTIONS] [NAME]...\n\n  Print information about SharePoint List(s)\n\n  NAME is not provided, all lists are returned.\n\nOptions:\n  -u, --url           TEXT  Sharepoint URL\n  -i, --client-id     TEXT  Client ID\n  -s, --client-secret TEXT  Client Secret\n  -t, --toml          FILE  TOML file with \'url\', \'client_id\', and \'client_secret\'\n  -f, --fields              include fields\n  --hidden                  include hidden lists (and fields)\n```\n\n## `netlink.sharepoint.base.Site`\n\nMain class representing a Sharepoint site. Can either be used directly providing the parameters\n\n- url\n- client_id\n- client_secret\n\nor inherited from\n\n```python\nfrom netlink.sharepoint.base import Site as _Site\n\n\nclass Site(_Site):\n    _url = "https://somewhere.sharepoint.com/sites/something"\n    _client_id = "00000000-0000-0000-0000-000000000000"\n    _client_secret = "abcdefghijklmnopqrstuvwxyz01234567890+/abcd="\n```\n\n### url\n\n_read-only_\n\n### users\n\n_read-only (always a copy of the actual data)_\n\nDict of the users of the site.\n\n| Column | Type | Description |\n|--------|:-----:|-----|\n| id | int | reference key for AuthorID, EditorID, etc. |\n| family_name | str | a.k.a. last name |\n| given_name | str | a.k.a. first name |\n| name | str | {family_name}, {given_name} |\n| email | str | |\n\n**Note** This is based on a default Sharepoint setup. This might not work for you.\n\n### get_list(name)\n\nReturns a Sharepoint List object (`office365.sharepoint.lists.list.List`) by **name**.\n\n### get_lists(hidden=False)\n\nReturns a list of Sharepoint List objects (`office365.sharepoint.lists.list.List`). If `hidden` is `True`, internal\nLists are included.\n\n### get_list_items(name)\n\nReturns list of all items (`office365.sharepoint.listitems.listitem.ListItem`) from **name**d Sharepoint List.\n\n### get_list_columns(name, hidden=False)\n\nReturns list of columns (a.k.a. Fields) of the **name**d Sharepoint List. If `hidden` is `True`, internal columns are\nincluded.\n\n### commit()\n\nSend all pending updates to Sharepoint.\n\n## `netlink.sharepoint.base.List`\n\nClass representing a Sharepoint List. This is a `collections.abc.Mapping`. Contents are mapped with the unique `id` of\nthe item in the Sharepoint List.\n\nWhen inherited from, class attribute\n\n- `_title` must be set.\n\n- `_map` should be set, but can be overridden. This maps the python name (best to use a valid attribute-name)\n  to the respective internal Sharepoint name. Do not map \'id\' or \'ID\', this is done automatically as the primary key.\n\n- `_upper_case` can be set to be used in `normalize` to enforce that the respective columns are set to uppercase.\n\n- `_required` can be set to ensure that the respective columns are not empty (as defined by Python: `None`, empty\n  string, or numeric zero).\n\nAt this point very optimistic (as in none-at-all) locking is used.\n\nThe item itself keeps information if data has been changed.\n\n### load()\n\nLoads all items from the Sharepoint List.\n\n### rollback()\n\nClears all local entries and calls `load`. At this time there is no difference, but when adding items will be supported,\nthis would clear them.\n\n### get(item, buffered=True)\n\nLoads (if nor already loaded) item based on unique `id`. If `buffered` is `False`, read from Sharepoint is forced.\n\n### commit()\n\nCommit all changed items to Sharepoint.\n\n### normalize()\n\nProcesses `_upper_case` for all items.\n\nConsider overriding this to set columns based on other columns.\n\n### validate()\n\nProcesses `_required` for all items.\n\nConsider overriding this to check list-wide constraints, like composite unique keys.\n\n## Item\n\nThis is a special class that gets build dynamically for each List. It is a `collections.abc.MutableMapping`.\n\nIt handles keeping state of changes and processes the actual mapping between Python and Sharepoint columns (fields).\n\n### commit(lazy=False)\n\nUpdate the internal `office365.sharepoint.listitems.listitem.ListItem` with any pending changes. If `lazy` is `True`,\nchanges are not sent to Sharepoint, providing the option to send on List or Site level.\n\n## License\n\nMIT\n',
    'author': 'Bernhard Radermacher',
    'author_email': 'bernhard.radermacher@netlink-consulting.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/netlink_python/netlink-sharepoint-base',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<=3.12',
}


setup(**setup_kwargs)
