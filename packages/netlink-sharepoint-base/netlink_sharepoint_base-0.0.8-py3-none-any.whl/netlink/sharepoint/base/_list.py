import collections.abc
import threading

from ._item import item_factory


class List(collections.abc.Mapping):
    """
    Class representing Sharepoint List

    When inherited from, class attribute _title must be set.

    _map should be set, but can be overridden. This maps the python name (best to use a valid attribute-name)
    to the respective internal Sharepoint name. Do not map 'id' or 'ID', this is done automatically as the primary key.

    _data contains records (class Item) with the key being the sharepoint ID.

    At this point very optimistic (as in none-at-all) locking is used.

    The item itself keeps information if data has been changed.
    """

    _title = ""
    _lock = threading.Lock()
    _map = {}
    _upper_case = None
    _required = None

    @property
    def title(self) -> str:
        return self._title

    def __init__(
        self, sharepoint_site, lazy: bool = True, title: str = None, map: dict = None, upper_case=None, required=None
    ):
        if not hasattr(self, "_sharepoint_site"):
            self._sharepoint_site = sharepoint_site
            self._title = title or self._title
            self._map = map or self._map
            self._upper_case = upper_case or self._upper_case
            self._required = required or self._required
            self._sharepoint_list = self._sharepoint_site.get_list(self.title)
            self._data = {}
            self._item_factory = item_factory(self)
        if not lazy:
            self.load()

    def load(self):
        for i in self._sharepoint_list.items.get_all().execute_query():
            item = self._item_factory(i)
            self._data[item.id] = item

    def rollback(self):
        self._data.clear()
        self.load()

    def get(self, item: int, buffered: bool = True):
        if not buffered or item not in self._data:
            item = self._item_factory(self._sharepoint_list.get_item_by_unique_id().execute_query())
            self._data[item.id] = item
        return self._data[id]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def commit(self):
        for i in self._data.values():
            i.commit(lazy=True)
        self._sharepoint_list.context.execute_batch()

    @property
    def python_map(self):
        return self._map.copy()

    @property
    def sharepoint_map(self):
        return {v: k for k, v in self._map.items()}

    def normalize(self):
        if self._upper_case:
            for i in self.values():
                for j in self._upper_case:
                    i[j] = i[j].upper()

    def validate(self):
        if self._required:
            errors = []
            for i in self.values():
                for j in self._required:
                    if not i[j]:
                        errors.append((i, j))

    def add_item(self, **kwargs):
        new_id = min(0, min(self._data)) - 1 if self._data else -1
        self._data[new_id] = self._item_factory(**kwargs)

    append = add_item
