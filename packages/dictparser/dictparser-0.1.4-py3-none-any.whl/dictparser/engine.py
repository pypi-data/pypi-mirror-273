import types
import typing
import collections.abc
import copy
import functools
import dataclasses
import sys
import yaml


_DATA = "__dictparser_data__"
_FROM_DICT_METHOD = "from_dict"
_FROM_FILE_METHOD = "from_file"
_AS_DICT_METHOD = "as_dict"


class MISSING:
    pass


class Data:
    def __init__(self):
        self.fields = {}
        self.result_cls = MISSING
        self.has_required = False
        self.ignore_extra = False


class Field:
    def __init__(self, field_name, field_type, data_key, default=MISSING, default_factory=MISSING):
        self.field_name = field_name
        self.field_type = field_type
        self.data_key = data_key
        self.default = None
        self.default_factory = None
        self.has_default = False
        self.required = True

        if default is not MISSING:
            self.has_default = True
            self.required = False
            self.default = default

        elif default_factory is not MISSING:
            self.has_default = True
            self.required = False
            self.default_factory = default_factory

    @classmethod
    def from_type(cls, field_name, field_type, default=MISSING):
        data_key = field_name
        default_factory = MISSING

        if default is not MISSING and default.__class__.__hash__ is None:
            def gen_factory(default):
                return lambda : copy.deepcopy(default)

            default_factory = gen_factory(default)
            default = MISSING

        if default is MISSING and default_factory is MISSING:
            if hasattr(field_type, _FROM_DICT_METHOD):
                default_factory = functools.partial(getattr(field_type, _FROM_DICT_METHOD), {})

        return cls(field_name, field_type, data_key, default=default, default_factory=default_factory)

    def get_value(self, data):
        return self.get_value_from_type(self.field_type, data)

    @classmethod
    def get_value_from_type(cls, field_type, data):
        if hasattr(field_type, _FROM_DICT_METHOD):
            method = getattr(field_type, _FROM_DICT_METHOD)
            return method(data)

        elif hasattr(field_type, "parse"):
            method = getattr(field_type, "parse")
            return method(data)

        elif field_type is None or field_type == type(None):
            if data is None:
                return None
            else:
                raise RuntimeError(f"Invalid data type '{data.__class__}' for field type of None")

        elif _get_origin(field_type) is not None:
            origin = _get_origin(field_type)

            if _is_union_type(field_type):
                args = _get_args(field_type)
                if len(args) == 2:
                    if args[0] is None or args[0] == type(None):
                        if data is None:
                            return None
                        else:
                            return cls.get_value_from_type(args[1], data)

                    elif args[1] is None or args[1] == type(None):
                        if data is None:
                            return None
                        else:
                            return cls.get_value_from_type(args[0], data)
                else:
                    raise NotImplementedError("Union type with <> 2 arguments is not supported")

            elif origin in (list, typing.List):
                args = _get_args(field_type)
                res = []
                for v in data:
                    res.append(cls.get_value_from_type(args[0], v))
                return res

            elif origin in (dict, typing.Dict):
                args = _get_args(field_type)
                res = {}
                for k, v in data.items():
                    res[k] = cls.get_value_from_type(args[1], v)
                return res

            else:
                raise NotImplementedError(f"'{origin}' not implemented")

        else:
            return field_type(data)

    def get_default(self):
        if self.default_factory:
            return self.default_factory()
        else:
            return self.default


def apply(cls, new_fields):
    fields = {}

    for base in cls.__mro__[-1:0:-1]:
        base_data = getattr(base, _DATA, None)
        if base_data is not None:
            for field in base_data.fields.values():
                fields[field.field_name] = field

    for new_field in new_fields.values():
        fields[new_field.field_name] = new_field

    #
    #
    #
    _data = Data()
    setattr(cls, _DATA, _data)

    _data.fields = fields

    for field in _data.fields.values():
        if not field.has_default:
            _data.has_required = True
            break

    _data.result_cls = cls

    #
    #
    #
    _setattr_method_from_dict(cls)
    _setattr_method_from_file(cls)
    _setattr_method_as_dict(cls)

    return dataclasses.dataclass(cls)


if sys.version_info >= (3, 10):
    def _get_origin(t):
        return typing.get_origin(t)


    def _is_union_type(t):
        origin = _get_origin(t)
        return origin in (types.UnionType, typing.Union)


    def _get_args(t):
        return list(typing.get_args(t))
else:
    def _get_origin(t):
        if hasattr(t, "__origin__"):
            return t.__origin__
        else:
            return None


    def _is_union_type(t):
        origin = _get_origin(t)
        return origin in (typing.Union, )


    def _get_args(t):
        return list(t.__args__)


def _setattr_method_from_dict(cls):
    if hasattr(cls, _FROM_DICT_METHOD):
        return

    def from_dict(cls, data):
        dictpaser_data = getattr(cls, _DATA)

        if not isinstance(data, collections.abc.Mapping):
            raise RuntimeError("data is not a dict like value")

        args = {}
        keys = set(data.keys())

        for field in dictpaser_data.fields.values():
            if field.data_key in data:
                args[field.field_name] = field.get_value(data[field.data_key])
                keys.remove(field.data_key)
            elif field.has_default:
                args[field.field_name] = field.get_default()
            elif field.required:
                raise RuntimeError(f"Required field '{field.field_name}' is missing")
            else:
                raise RuntimeError("ups")

        if len(keys) > 0 and not dictpaser_data.ignore_extra:
            raise RuntimeError(f"Extra data keys: {list(keys)}")

        result_cls = dictpaser_data.result_cls
        return result_cls(**args)

    from_dict.__qualname__ = f"{cls.__qualname__}.from_dict"

    setattr(cls, _FROM_DICT_METHOD, classmethod(from_dict))


def _setattr_method_from_file(cls):
    if hasattr(cls, _FROM_FILE_METHOD):
        return

    def from_file(cls, file):
        with open(file, "rt", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls.from_dict(data)

    from_file.__qualname__ = f"{cls.__qualname__}.from_file"

    setattr(cls, _FROM_FILE_METHOD, classmethod(from_file))


def _setattr_method_as_dict(cls):
    if hasattr(cls, _AS_DICT_METHOD):
        return

    def as_dict(self):
        return dataclasses.asdict(self)

    as_dict.__qualname__ = f"{cls.__qualname__}.as_dict"

    setattr(cls, _AS_DICT_METHOD, as_dict)
