from .engine import Field
from .engine import apply as _apply


def dictparser(cls):
    fields = {}

    if hasattr(cls, "__annotations__"):
        for field_name, field_type in cls.__annotations__.items():
            if hasattr(cls, field_name):
                default = getattr(cls, field_name)
                delattr(cls, field_name)
                field = Field.from_type(field_name, field_type, default)
            else:
                field = Field.from_type(field_name, field_type)

            fields[field.field_name] = field

    return _apply(cls, fields)
