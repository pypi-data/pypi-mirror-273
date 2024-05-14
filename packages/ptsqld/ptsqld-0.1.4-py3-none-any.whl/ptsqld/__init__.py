from os.path import exists
from datetime import datetime
from functools import partialmethod
from dulwich.object_store import DiskObjectStore, MemoryObjectStore
from dulwich.refs import DiskRefsContainer, DictRefsContainer
from random import choices
from string import ascii_letters, digits
from weakref import WeakSet
from .structured_engine import Engine
from .structured_vault import Vault

def __forward(self, method_name, *args, **kwargs):
    return getattr(self._engine, method_name)(*args, *kwargs)


class Cursor:
    def __init__(self, tables):
        self._engine = Engine(tables)

    def __iter__(self):
        yield from iter(self._engine)

    @property
    def description(self):
        return self._engine.description

    def close(self):
        ...

class Connection:
    def __init__(self, path, branch='main'):
        self.__branches = WeakSet()
        
        if path == ':memory:':
            object_store = MemoryObjectStore()
            refs_container = DictRefsContainer({})
        else:
            if not exists(path):
                raise ValueError(f'No such git repositories found at {path}')
            
            if exists(path + '/.git'):
                path += '/.git/'

            object_store = DiskObjectStore(path + '/objects/')
            refs_container = DiskRefsContainer(path + '/')
            
        self.__tables = Vault(object_store, refs_container)

        try:
            self.__tables.checkout(branch)
        except ValueError:
            # init branch if not existing
            self.__tables.commit(branch)
            self.__tables.checkout(branch, True)

        self._engine = Engine(self.__tables)

    def close(self):
        ...

    def commit(self):
        message = f'update at {datetime.now().isoformat()}'
        
        for branch in self.__branches:
            branch.commit(message=message)
            
        if self.__branches:
            self.__tables.merge(self.__branches)
        
        self.__tables.commit(message=(f'merge {self.__tables.ref} with {tuple(branch.ref for branch in self.__branches)}'
                                      if self.__branches
                                      else message))
        
        for branch in self.__branches:
            branch.merge((self.__tables,))

    def rollback(self):
        self.__tables.rollback()

    def cursor(self):
        tables = Vault(self.__tables.object_store,
                       self.__tables.refs,
                       ref=self.__tables.ref)
        
        ref = (tables.ref
               + '_'
               + ''.join(choices(tuple(set(digits)
                                       | set(ascii_letters)),
                                 k=8)))
        tables.checkout(ref, branch=True)
        
        self.__branches.add(tables)
        
        return Cursor(tables)

    @property
    def description(self):
        return self._engine.description

for method_name in {'execute', 'fetchone', 'fetchmany', 'fetchall'}:
    setattr(Cursor, method_name, partialmethod(__forward, method_name))
    setattr(Connection, method_name, partialmethod(__forward, method_name))

def connect(path):
    return Connection(path)
