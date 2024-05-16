from itertools import chain
from types import GenericAlias
from weakref import WeakValueDictionary

from pydantic import parse_obj_as


class TypeParametersMemoizer(type):
    _generics_cache = WeakValueDictionary()

    def __getitem__(cls, typeparams):
        # prevent duplication of generic types
        if typeparams in cls._generics_cache:
            return cls._generics_cache[typeparams]

        # middleware class for holding type parameters
        class TypeParamsWrapper(cls):
            __type_parameters__ = typeparams if isinstance(typeparams, tuple) else (typeparams,)

            @classmethod
            def _get_type_parameters(cls):
                return cls.__type_parameters__

        return GenericAlias(TypeParamsWrapper, typeparams)


class CommaSeparatedList(list, metaclass=TypeParametersMemoizer):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str | list[str]):
        if isinstance(v, str):
            v = v.split(",")
        else:
            v = list(chain.from_iterable((x.split(",") for x in v)))
        params = cls._get_type_parameters()
        return parse_obj_as(list[params], list(map(str.strip, v)))

    @classmethod
    def _get_type_parameters(cls):
        raise NotImplementedError("should be overridden in metaclass")
