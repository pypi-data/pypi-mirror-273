import collections.abc

from office365.sharepoint.listitems.listitem import ListItem
from netlink.logging import logger


def item_factory(sharepoint_list):
    _len = len(sharepoint_list.sharepoint_map) + 1
    _iter = [i for i in sharepoint_list.python_map]
    _iter.insert(0, "id")
    _iter = tuple(_iter)

    class Item(collections.abc.MutableMapping):
        _sharepoint_list = sharepoint_list

        # noinspection PyProtectedMember
        def __init__(self, *args, **kwargs):
            if args:
                if isinstance(args[0], ListItem):
                    self._list_item: ListItem = args[0]
                    self._data = dict(id=self._list_item.id)
                else:
                    raise ValueError
            else:
                new_args = {s: kwargs[p] for p, s in self._sharepoint_list._map.items() if p in kwargs}
                self._list_item = self._sharepoint_list._sharepoint_list.add_item(new_args)
                self._data = dict(id=None)
            for sharepoint_column in self._sharepoint_list.sharepoint_map:
                v = self._list_item.get_property(sharepoint_column)
                python_column = self._sharepoint_list.sharepoint_map[sharepoint_column]
                logger.trace(f"{sharepoint_column}: {v} -> {python_column}")
                self._data[python_column] = v
            self._dirty = set()

        def __len__(self) -> int:
            return _len

        def __iter__(self):
            return iter(_iter)

        def __getitem__(self, item):
            if item in _iter:
                return self._data.get(item, None)
            raise KeyError(item)

        def __setitem__(self, key, value):
            # id cannot be changed
            if key in self._sharepoint_list.python_map:
                if self._data.get(key, None) != value:
                    self._data[key] = value
                    self._dirty.add(key)
            else:
                raise KeyError(key)

        def __delitem__(self, key):
            raise NotImplementedError

        def __getattr__(self, item):
            try:
                return self[item]
            except KeyError:
                raise AttributeError(item)

        def commit(self, lazy: bool = False):
            if self._dirty or self.id is None:
                for i in self._dirty:
                    self._list_item.set_property(self._sharepoint_list.python_map[i], self._data[i]).update()
                self._dirty.clear()
                if not lazy:
                    self._list_item.execute_query()

        def __repr__(self):
            return f"{self._sharepoint_list.title}: {self._data}"

    return Item
