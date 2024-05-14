from random import randint
from echovault import Vault as _Vault 
from echovault.list import List as _List 
from echovault.dict import Dict as _Dict 

class Vault(_Vault):
    class List(_List):
        class Dict(_Dict):
            def __setitem__(self, key, value):
                table_name = self.container.identifier

                if table_name == b'__schema':
                    super().__setitem__(key, value)
                    return
                
                (_, schema), = (table
                                for table in self.container.container['__schema']
                                if table['name'] == table_name)

                if key not in schema.keys():
                    raise KeyError(f"{key} not one of the keys part of table {table_name} schema")

                super().__setitem__(key, value)

        def extend(self, iterable):
            table_name = self.identifier.decode('utf-8')

            if table_name == '__schema':
                super().extend(iterable)
                return
            
            def filler(iterable):
                for table in self.container['__schema']:
                    if table['name'] == table_name:
                        break
                else:
                    raise KeyError(f'No table {table_name} in schema')

                schema = table['description']
                
                for entry in iterable:
                    _entry = {} | entry
                    
                    if unexpected_keys := (set(entry.keys()) - set(schema.keys())):
                        raise KeyValue(f'those {unexpected_keys} keys are not expected in table {table_name}')
                    
                    for key in set(schema.keys()) - set(entry.keys()):
                        description = schema[key]
                        
                        for _, constraint in description[1]:
                            if constraint.get("autoincrement", False):
                                value = randint(0, 2**64)
                                break
                        else:
                            value = None
                            
                        _entry[key] = value

                    yield _entry

            super().extend(filler(iterable))

    def diff(self, other):
        if self.tree.id == other.tree.id:
            return

        if '__schema' in self.keys() and '__schema' not in other.keys():
            yield ('+', {'__schema':self['__schema']})
        elif '__schema' not in self.keys() and '__schema' in other.keys():
            yield ('-', {'__schema'})
        elif '__schema' in self.keys() and '__schema' in other.keys():
            for difference in self['__schema'].diff(other['__schema']):
                yield ('!=', '__schema', *difference)
        
        for difference in super().diff(other):
            match difference:
                case ('+', added):
                    added.pop('__schema')
                    yield ('+', added)
                case ('-', removed):
                    yield ('-', removed - {'__schema'})
                case ('!=', table, *rest):
                    if table != '__schema':
                        yield ('!=', table, *rest)
