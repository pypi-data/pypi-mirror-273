#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#An ORM/ODM for Google Cloud Datastore/MongoDB/redis, featuring a compatible interface with Peewee.
#Author: cdhigh <http://github.com/cdhigh>
#Repository: <https://github.com/cdhigh/weedata>
#Pypi package: <https://pypi.org/project/weedata>
import copy
from .fields import (Field, FieldDescriptor, PrimaryKeyField, ForeignKeyField, DoesNotExist, 
        Filter, JSONField)
from .queries import (QueryBuilder, DeleteQueryBuilder, InsertQueryBuilder, UpdateQueryBuilder,
    ReplaceQueryBuilder)

class BaseModel(type):
    inheritable_options = ['client', 'order_by', 'primary_key']

    def __new__(cls, name, bases, attrs):
        if not bases:
            return super(BaseModel, cls).__new__(cls, name, bases, attrs) # pragma: no cover

        meta_options = {}
        meta = attrs.pop('Meta', None)
        if meta:
            meta_options.update((k, v) for k, v in meta.__dict__.items() if not k.startswith('_'))
            #for compatibilty, app code use the name "database", convert to "client" here
            if 'database' in meta_options:
                meta_options['client'] = meta_options.pop('database', None)

        for b in bases:
            base_meta = getattr(b, '_meta', None)
            if not base_meta:
                continue
            
            for (k, v) in base_meta.__dict__.items():
                if k in cls.inheritable_options and k not in meta_options:
                    meta_options[k] = v

            for (k, v) in b.__dict__.items():
                if isinstance(v, FieldDescriptor) and k not in attrs:
                    attrs[k] = copy.deepcopy(v.field_inst)

        meta_options.setdefault('client', None)
        meta_options.setdefault('primary_key', 'id')
        attrs[meta_options['primary_key']] = PrimaryKeyField()

        # initialize the new class and set the magic attributes
        cls = super(BaseModel, cls).__new__(cls, name, bases, attrs)
        cls._meta = ModelOptions(cls, **meta_options)
        cls._data = None
        cls._dirty = None

        # replace the fields with field descriptors, calling the add_to_class hook
        bytes_store = meta_options['client'].bytes_store if meta_options['client'] else False
        for name, attr in cls.__dict__.items():
            if isinstance(attr, Field):
                attr.add_to_class(cls, name, bytes_store)
        
        cls._meta.prepared()
        return cls

class ModelOptions(object):
    def __init__(self, cls, client=None, order_by=None, primary_key='id', **kwargs):
        self.model_class = cls
        self.name = cls.__name__
        self.fields = {}
        self.defaults = {}
        self.client = client #database here is actually a database client
        self.order_by = order_by
        self.primary_key = primary_key
        self.backref = {}
        self.exclude_from_indexes = [] #for datastore only
        
    def prepared(self):
        for field in self.fields.values():
            if field.default is not None:
                self.defaults[field] = field.default
            if field.index == False: #will be indexed when is None/True in datastore
                self.exclude_from_indexes.append(field.name)

class Model(object, metaclass=BaseModel):
    def __init__(self, **kwargs):
        self._key = kwargs.get('_key', None)
        self._data = {f.name: v() for f, v in self._meta.defaults.items()}
        self._obj_cache = {} # cache of foreign_key objects
        self._dirty = {'__key__': True, '_id': True}
        for name, value in kwargs.items():
            setattr(self, name, value)

    @classmethod
    def create(cls, **kwargs):
        inst = cls(**kwargs)
        return inst.save()

    @classmethod
    def select(cls, *args):
        return QueryBuilder(cls, *args)

    @classmethod
    def delete(cls):
        return DeleteQueryBuilder(cls)

    @classmethod
    def update(cls, *args, **kwargs):
        return UpdateQueryBuilder(cls, cls.combine_args_kwargs(*args, **kwargs))

    @classmethod
    def insert(cls, *args, **kwargs):
        return InsertQueryBuilder(cls, cls.combine_args_kwargs(*args, **kwargs))
        
    @classmethod
    def insert_many(cls, datas: list):
        return InsertQueryBuilder(cls, datas)

    @classmethod
    def replace(cls, *args, **kwargs):
        return ReplaceQueryBuilder(cls, cls.combine_args_kwargs(*args, **kwargs))

    @classmethod
    def combine_args_kwargs(cls, *args, **kwargs):
        if (len(args) > 1) or (args and not isinstance(args[0], dict)):
            raise ValueError('The keyword argument have to be a dict')
        args = args[0] if args else {}
        args.update(kwargs)
        return dict(((f.name if isinstance(f, Field) else f), v) for f, v in args.items())
        
    @classmethod
    def get(cls, *query, **filters):
        sq = cls.select()
        if query:
            # Handle simple lookup using just the primary key.
            if len(query) == 1 and isinstance(query[0], str):
                sq = sq.filter_by_id(query[0])
            else:
                sq = sq.where(*query)
        for item, value in filters.items():
            sq = sq.where(Filter(item, Filter.EQ, value))
        return sq.get()

    @classmethod
    def get_or_create(cls, **kwargs):
        defaults = kwargs.pop('defaults', {})
        query = cls.select()
        for field, value in kwargs.items():
            query = query.where(getattr(cls, field) == value)

        model = query.get()
        if model:
            return model, False
        else:
            if defaults:
                kwargs.update(defaults)
            with cls._meta.client.atomic():
                return cls.create(**kwargs), True

    @classmethod
    def get_or_none(cls, *query, **filters):
        try:
            return cls.get(*query, **filters)
        except: # pragma: no cover
            return None

    @classmethod
    def get_by_key(cls, key):
        return cls.select().filter_by_key(key).first()

    @classmethod
    def get_by_id(cls, sid):
        return cls.select().filter_by_id(sid).first()

    @classmethod
    def delete_by_id(cls, pk):
        return cls.delete().filter_by_id(pk).execute()
        
    def save(self, **kwargs):
        return self.client.update_one(self)
        
    def delete_instance(self, **kwargs):
        #foreign keys on delete cascade
        for field in [f for f in self._meta.backref.values() if f.on_delete]:
            field.model.delete().where(field == self.get_id()).execute()
        self.client.delete_one(self)

    @property
    def client(self):
        return self._meta.client

    #Convert model into a dict
    #: params only=[Model.title, ...]
    #: params exclude=[Model.title, ...]
    #: remove_id - remove key and id field from dict
    #: db_value - if prepared for saving to db
    #: only_dirty - export items unsaved only
    def dicts(self, only=None, exclude=None, remove_id=False, db_value=False, only_dirty=False):
        only = [(x if isinstance(x, str) else x.name) for x in (only or [])]
        exclude = [(x if isinstance(x, str) else x.name) for x in (exclude or [])]
        should_skip = lambda n: (n in exclude) or (only and (n not in only))
        
        data = {}
        for name, field in self._meta.fields.items():
            if should_skip(name):
                continue
            
            # JSONField is mutable and sometimes its changes cannot be determined
            if not only_dirty or (self._dirty.get(name) or isinstance(field, JSONField)):
                value = getattr(self, name, None)
                if value and isinstance(field, ForeignKeyField) and isinstance(value, Model):
                    value = value.get_id()
                if db_value:
                    value = field.db_value(value)
                data[name] = value

        if remove_id:
            data.pop('_key', None)
            data.pop('id', None)
            data.pop('_id', None)
        self.client.log.debug(self._meta.name + '.dicts: \n' + str(data))
        return data

    @classmethod
    def bind(cls, client):
        cls._meta.client = client
        for field in cls._meta.fields.values():
            field.bytes_store = client.bytes_store
    
    #Used for create index
    #MongoDB Create index commands will not recreate existing indexes and 
    #instead return a success message indicating "all indexes already exist"
    @classmethod
    def create_table(cls, **kwargs):
        for name, field in cls._meta.fields.items():
            if field.index or field.unique:
                cls._meta.client.create_index(cls, name, unique=field.unique, background=True)

    def clear_dirty(self, field_name):
        field_name = field_name if isinstance(field_name, list) else [field_name]
        excluded = ['__key__', '_id', self.client.db_id_name()]
        for name in field_name:
            if name not in excluded:
                self._dirty[name] = False

    def get_id(self):
        return getattr(self, self._meta.primary_key, None)

    def set_id(self, value):
        setattr(self, self._meta.primary_key, value)
        return self

    #will return True if you change the value of an indexed field
    #param: other - a model instance will be save to database
    def index_changed(self, other):
        assert(other._meta.name == self._meta.name)
        for name, field in self._meta.fields.items():
            if (field.index or field.unique) and (getattr(self, name, None) != getattr(other, name, None)):
                return True
        return False
