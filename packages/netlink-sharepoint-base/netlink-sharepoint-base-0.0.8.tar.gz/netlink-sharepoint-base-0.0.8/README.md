# netlink-sharepoint-base

## Basic Tools for interaction with Sharepoint Sites

This has been moved from `netlink-sharepoint`

For now only **Lists** are considered.

## `sharepoint_list_info`

Script to help mapping

```shell
Usage: sharepoint_list_info.py [OPTIONS] [NAME]...

  Print information about SharePoint List(s)

  NAME is not provided, all lists are returned.

Options:
  -u, --url           TEXT  Sharepoint URL
  -i, --client-id     TEXT  Client ID
  -s, --client-secret TEXT  Client Secret
  -t, --toml          FILE  TOML file with 'url', 'client_id', and 'client_secret'
  -f, --fields              include fields
  --hidden                  include hidden lists (and fields)
```

## `netlink.sharepoint.base.Site`

Main class representing a Sharepoint site. Can either be used directly providing the parameters

- url
- client_id
- client_secret

or inherited from

```python
from netlink.sharepoint.base import Site as _Site


class Site(_Site):
    _url = "https://somewhere.sharepoint.com/sites/something"
    _client_id = "00000000-0000-0000-0000-000000000000"
    _client_secret = "abcdefghijklmnopqrstuvwxyz01234567890+/abcd="
```

### url

_read-only_

### users

_read-only (always a copy of the actual data)_

Dict of the users of the site.

| Column | Type | Description |
|--------|:-----:|-----|
| id | int | reference key for AuthorID, EditorID, etc. |
| family_name | str | a.k.a. last name |
| given_name | str | a.k.a. first name |
| name | str | {family_name}, {given_name} |
| email | str | |

**Note** This is based on a default Sharepoint setup. This might not work for you.

### get_list(name)

Returns a Sharepoint List object (`office365.sharepoint.lists.list.List`) by **name**.

### get_lists(hidden=False)

Returns a list of Sharepoint List objects (`office365.sharepoint.lists.list.List`). If `hidden` is `True`, internal
Lists are included.

### get_list_items(name)

Returns list of all items (`office365.sharepoint.listitems.listitem.ListItem`) from **name**d Sharepoint List.

### get_list_columns(name, hidden=False)

Returns list of columns (a.k.a. Fields) of the **name**d Sharepoint List. If `hidden` is `True`, internal columns are
included.

### commit()

Send all pending updates to Sharepoint.

## `netlink.sharepoint.base.List`

Class representing a Sharepoint List. This is a `collections.abc.Mapping`. Contents are mapped with the unique `id` of
the item in the Sharepoint List.

When inherited from, class attribute

- `_title` must be set.

- `_map` should be set, but can be overridden. This maps the python name (best to use a valid attribute-name)
  to the respective internal Sharepoint name. Do not map 'id' or 'ID', this is done automatically as the primary key.

- `_upper_case` can be set to be used in `normalize` to enforce that the respective columns are set to uppercase.

- `_required` can be set to ensure that the respective columns are not empty (as defined by Python: `None`, empty
  string, or numeric zero).

At this point very optimistic (as in none-at-all) locking is used.

The item itself keeps information if data has been changed.

### load()

Loads all items from the Sharepoint List.

### rollback()

Clears all local entries and calls `load`. At this time there is no difference, but when adding items will be supported,
this would clear them.

### get(item, buffered=True)

Loads (if nor already loaded) item based on unique `id`. If `buffered` is `False`, read from Sharepoint is forced.

### commit()

Commit all changed items to Sharepoint.

### normalize()

Processes `_upper_case` for all items.

Consider overriding this to set columns based on other columns.

### validate()

Processes `_required` for all items.

Consider overriding this to check list-wide constraints, like composite unique keys.

## Item

This is a special class that gets build dynamically for each List. It is a `collections.abc.MutableMapping`.

It handles keeping state of changes and processes the actual mapping between Python and Sharepoint columns (fields).

### commit(lazy=False)

Update the internal `office365.sharepoint.listitems.listitem.ListItem` with any pending changes. If `lazy` is `True`,
changes are not sent to Sharepoint, providing the option to send on List or Site level.

## License

MIT
