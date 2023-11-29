import ast
from enum import Enum
from typing import Optional, List


def skip(func):
    return func


@skip
def represent_class(obj, represent_args: bool = False, represent_keywords: bool = False,
                    represent_as_value: bool = False, only_use_attributes: Optional[List[str]] = None):
    func_name = obj._dataflow_name if hasattr(obj, "_dataflow_name") else obj.__class__.__name__

    attributes = {}
    for attr in [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("_")]:
        if only_use_attributes and attr not in only_use_attributes:
            continue
        attr_value = getattr(obj, attr)
        if type(attr_value) is str or type(attr_value) is int or type(attr_value) is float:
            attributes[attr] = ast.Name(id=str(attr_value))
        elif attr_value is not None:
            attributes[attr] = attr_value.func_repr()

    if represent_args:
        return [ast.Call(
            func=ast.Name(id=func_name),
            args=[attr_value for attr_value in attributes.values()],
            keywords=[]
        )]
    elif represent_keywords:
        return [ast.Call(
            func=ast.Name(id=func_name),
            args=[],
            keywords=[ast.keyword(arg=attr, value=attr_value) for attr, attr_value in attributes.items()]
        )]
    elif represent_as_value:
        return [ast.alias(name=func_name)]


class RepresentEnumValue:
    def __init__(self, name):
        self.name = name

    def func_repr(self):
        return [ast.Call(
            func=ast.Name(id=self.name),
            args=[],
            keywords=[]
        )]


class RepresentEnum(Enum):
    def __get__(self, instance, owner):
        return RepresentEnumValue(self.name)

@skip
class RepresentArgs:
    def func_repr(self):
        return represent_class(self, represent_args=True)


@skip
class RepresentKeywords:
    def func_repr(self):
        return represent_class(self, represent_keywords=True)


@skip
class RepresentValue:
    def func_repr(self):
        return represent_class(self, represent_as_value=True)
