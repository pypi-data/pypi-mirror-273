from ..utils import solidipes_logging as logging

logger = logging.getLogger()

################################################################


def wrap_errors(func):
    def foo(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            self.errors.append(str(e))

    return foo


################################################################


class DataContainer:
    """Container class for other structured data containers"""

    def __init__(self, initial_data={}, name=None, unique_identifier=None, **kwargs):
        logger.debug(f"Creating data container {type(self)}")
        self.name = None
        self.unique_identifier = unique_identifier

        #: Dictionary of other DataContainer or arbitrary objects.
        #: Set entry to "None" to mark as loadable.
        self._data_collection = initial_data.copy()
        clss = set([self.__class__])
        while clss:
            new_clss = set()
            for cls in clss:
                for key, v in cls.__dict__.items():
                    if isinstance(v, DataContainer.loadable):
                        if key not in self._data_collection:
                            self.add(key)
                for c in cls.__bases__:
                    new_clss.add(c)
            clss = new_clss

        #: Default viewer for this file. Optionally override this in
        #: subclasses.
        self.default_viewer = None

        #: stores the error messages during loading
        self.errors = []

    def _valid_loading(self):
        if self.errors:
            return False
        return True

    def copy(self):
        """Returns a shallow copy without the need to read from disk again"""
        cls = self.__class__
        new = cls.__new__(cls)
        new.__dict__.update(self.__dict__)
        new._data_collection = self._data_collection.copy()
        return new

    @property
    def data_info(self):
        """Returns a multi-line string with information about data keys"""
        info_list = []

        for key, data in self._data_collection.items():
            if data is None:
                info_list.append(f"{key}: Not loaded")
            else:
                info_list.append(f"{key}: {type(self._data_collection[key])}")

        return "\n".join(info_list)

    @property
    def data(self):
        """Load all data if necessary and return it

        Accessing this property for the first time will load the data.
        If self.__loaded_data has only one entry, returns it directly.

        Override the _load_data method in subclasses to define how data is
        loaded or built using other data containers.
        """
        self.load_all()

        # Return data
        if len(self._data_collection) == 1:
            return list(self._data_collection.values())[0]
        else:
            return self._data_collection

    @wrap_errors
    def load_all(self):
        """Load all data"""
        # Find keys that have a None value and load them
        keys = [e for e in self._data_collection.keys()]
        for key in keys:
            if self._data_collection[key] is None:
                # Trigger loading of data
                self.get(key)

    def add(self, key, data=None):
        """Add an arbitrary object to the data collection"""
        self._data_collection[key] = data

    def get(self, key):
        """Get a data object by key, loading it if necessary"""

        logger.debug(f"get({key})")
        try:
            data = self._data_collection[key]
        except KeyError as e:
            raise KeyError(f"{e}\nDid you register this key somehow ?")

        # Load data
        if data is None:
            data = getattr(self, key)
            if data is None:
                raise Exception(f'Data "{key}" could not be loaded')
            self._data_collection[key] = data

        logger.debug(f"got({key}) = {data}")
        return data

    def remove(self, key):
        """Remove a data object from the data collection"""
        del self._data_collection[key]

    def has(self, key):
        """Check if data is available in this container"""
        return key in self._data_collection

    def _has_native_attr(self, key):
        """Check if attribute is present, outside of _data_collection, without using __getattr__"""

        try:
            self.__getattribute__(key)
            return True
        except AttributeError:
            return False

    def __getattr__(self, name):
        """Get a data object by key, loading it if necessary

        Only works if the name is not already an attribute of this class.
        """

        try:
            return self.get(name)
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")

    def view(self, **kwargs):
        """View the file using the default viewer"""

        if self.default_viewer is None:
            raise Exception("This File cannot be viewed directly. Use get_data to get a Dataobject.")
        viewer = self.default_viewer(self, **kwargs)
        return viewer

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self._data_collection.__repr__()

    class loadable(property):
        def __init__(self, func):
            key = func.__name__

            def foo(obj, *args, **kwargs):
                logger.debug(obj)
                if key in obj._data_collection and obj._data_collection[key] is not None:
                    return obj._data_collection[key]
                data = func(obj, *args, **kwargs)
                if data is None:
                    raise Exception(f'Data "{key}" could not be loaded')
                obj._data_collection[key] = data
                return data

            def foo_setter(obj, value, *args, **kwargs):
                obj._data_collection[key] = value

            super().__init__(foo, foo_setter)


################################################################
