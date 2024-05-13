# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Copyright the Hypothesis Authors.
# Individual contributors are listed in AUTHORS.rst and the git log.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.

import builtins
import collections
import collections.abc
import datetime
import decimal
import fractions
import functools
import inspect
import io
import ipaddress
import numbers
import operator
import os
import random
import re
import sys
import typing
import uuid
import warnings
from functools import partial
from pathlib import PurePath
from types import FunctionType
from typing import TYPE_CHECKING, Any, Iterator, Tuple, get_args, get_origin

from hypothesis import strategies as st
from hypothesis.errors import HypothesisWarning, InvalidArgument, ResolutionFailed
from hypothesis.internal.compat import PYPY, BaseExceptionGroup, ExceptionGroup
from hypothesis.internal.conjecture.utils import many as conjecture_utils_many
from hypothesis.internal.filtering import max_len, min_len
from hypothesis.internal.reflection import get_pretty_function_description
from hypothesis.strategies._internal.datetime import zoneinfo  # type: ignore
from hypothesis.strategies._internal.ipaddress import (
    SPECIAL_IPv4_RANGES,
    SPECIAL_IPv6_RANGES,
    ip_addresses,
)
from hypothesis.strategies._internal.lazy import unwrap_strategies
from hypothesis.strategies._internal.strategies import OneOfStrategy

if TYPE_CHECKING:
    import annotated_types as at

GenericAlias: typing.Any
UnionType: typing.Any
try:
    # The type of PEP-604 unions (`int | str`), added in Python 3.10
    from types import GenericAlias, UnionType
except ImportError:
    GenericAlias = ()
    UnionType = ()

try:
    import typing_extensions
except ImportError:
    typing_extensions = None  # type: ignore

try:
    from typing import _AnnotatedAlias  # type: ignore
except ImportError:
    try:
        from typing_extensions import _AnnotatedAlias
    except ImportError:
        _AnnotatedAlias = ()

TypeAliasTypes: tuple = ()
try:
    TypeAliasTypes += (typing.TypeAlias,)
except AttributeError:  # pragma: no cover
    pass  # Is missing for `python<3.10`
try:
    TypeAliasTypes += (typing_extensions.TypeAlias,)
except AttributeError:  # pragma: no cover
    pass  # Is missing for `typing_extensions<3.10`

ClassVarTypes: tuple = (typing.ClassVar,)
try:
    ClassVarTypes += (typing_extensions.ClassVar,)
except AttributeError:  # pragma: no cover
    pass  # `typing_extensions` might not be installed

FinalTypes: tuple = (typing.Final,)
try:
    FinalTypes += (typing_extensions.Final,)
except AttributeError:  # pragma: no cover
    pass  # `typing_extensions` might not be installed

ConcatenateTypes: tuple = ()
try:
    ConcatenateTypes += (typing.Concatenate,)
except AttributeError:  # pragma: no cover
    pass  # Is missing for `python<3.10`
try:
    ConcatenateTypes += (typing_extensions.Concatenate,)
except AttributeError:  # pragma: no cover
    pass  # `typing_extensions` might not be installed

ParamSpecTypes: tuple = ()
try:
    ParamSpecTypes += (typing.ParamSpec,)
except AttributeError:  # pragma: no cover
    pass  # Is missing for `python<3.10`
try:
    ParamSpecTypes += (typing_extensions.ParamSpec,)
except AttributeError:  # pragma: no cover
    pass  # `typing_extensions` might not be installed

TypeGuardTypes: tuple = ()
try:
    TypeGuardTypes += (typing.TypeGuard,)
except AttributeError:  # pragma: no cover
    pass  # Is missing for `python<3.10`
try:
    TypeGuardTypes += (typing_extensions.TypeGuard,)
except AttributeError:  # pragma: no cover
    pass  # `typing_extensions` might not be installed


RequiredTypes: tuple = ()
try:
    RequiredTypes += (typing.Required,)  # type: ignore
except AttributeError:  # pragma: no cover
    pass  # Is missing for `python<3.11`
try:
    RequiredTypes += (typing_extensions.Required,)
except AttributeError:  # pragma: no cover
    pass  # `typing_extensions` might not be installed


NotRequiredTypes: tuple = ()
try:
    NotRequiredTypes += (typing.NotRequired,)  # type: ignore
except AttributeError:  # pragma: no cover
    pass  # Is missing for `python<3.11`
try:
    NotRequiredTypes += (typing_extensions.NotRequired,)
except AttributeError:  # pragma: no cover
    pass  # `typing_extensions` might not be installed


# We use this variable to be sure that we are working with a type from `typing`:
typing_root_type = (typing._Final, typing._GenericAlias)  # type: ignore

# We use this to disallow all non-runtime types from being registered and resolved.
# By "non-runtime" we mean: types that do not really exist in python's
# and are just added for more fancy type annotations.
# `Final` is a great example: it just indicates that this value can't be reassigned.
NON_RUNTIME_TYPES = (
    typing.Any,
    *ClassVarTypes,
    *TypeAliasTypes,
    *FinalTypes,
    *ConcatenateTypes,
    *ParamSpecTypes,
    *TypeGuardTypes,
)
for name in (
    "Annotated",
    "NoReturn",
    "Self",
    "Required",
    "NotRequired",
    "Never",
    "TypeVarTuple",
    "Unpack",
    "LiteralString",
):
    try:
        NON_RUNTIME_TYPES += (getattr(typing, name),)
    except AttributeError:
        pass
    try:
        NON_RUNTIME_TYPES += (getattr(typing_extensions, name),)
    except AttributeError:  # pragma: no cover
        pass  # typing_extensions might not be installed


def type_sorting_key(t):
    """Minimise to None, then non-container types, then container types."""
    if t is None or t is type(None):
        return (-1, repr(t))
    t = get_origin(t) or t
    try:
        is_container = int(issubclass(t, collections.abc.Container))
    except Exception:  # pragma: no cover
        # e.g. `typing_extensions.Literal` is not a container
        is_container = 0
    return (is_container, repr(t))


def _compatible_args(args, superclass_args):
    """Check that the args of two generic types are compatible for try_issubclass."""
    assert superclass_args is not None
    if args is None:
        return True
    return len(args) == len(superclass_args) and all(
        # "a==b or either is a typevar" is a hacky approximation, but it's
        # good enough for all the cases that I've seen so far and has the
        # substantial virtue of (relative) simplicity.
        a == b or isinstance(a, typing.TypeVar) or isinstance(b, typing.TypeVar)
        for a, b in zip(args, superclass_args)
    )


def try_issubclass(thing, superclass):
    try:
        # In this case we're looking at two distinct classes - which might be generics.
        # That brings in some complications:
        if issubclass(get_origin(thing) or thing, get_origin(superclass) or superclass):
            superclass_args = get_args(superclass)
            if not superclass_args:
                # The superclass is not generic, so we're definitely a subclass.
                return True
            # Sadly this is just some really fiddly logic to handle all the cases
            # of user-defined generic types, types inheriting from parametrised
            # generics, and so on.  If you need to change this code, read PEP-560
            # and Hypothesis issue #2951 closely first, and good luck.  The tests
            # will help you, I hope - good luck.
            if getattr(thing, "__args__", None) is not None:
                return True  # pragma: no cover  # only possible on Python <= 3.9
            for orig_base in getattr(thing, "__orig_bases__", None) or [None]:
                args = getattr(orig_base, "__args__", None)
                if _compatible_args(args, superclass_args):
                    return True
        return False
    except (AttributeError, TypeError):
        # Some types can't be the subject or object of an instance or subclass check
        return False


def is_a_new_type(thing):
    if not isinstance(typing.NewType, type):
        # At runtime, `typing.NewType` returns an identity function rather
        # than an actual type, but we can check whether that thing matches.
        return (  # pragma: no cover  # Python <= 3.9 only
            hasattr(thing, "__supertype__")
            and getattr(thing, "__module__", None) in ("typing", "typing_extensions")
            and inspect.isfunction(thing)
        )
    # In 3.10 and later, NewType is actually a class - which simplifies things.
    # See https://bugs.python.org/issue44353 for links to the various patches.
    return isinstance(thing, typing.NewType)


def is_a_union(thing):
    """Return True if thing is a typing.Union or types.UnionType (in py310)."""
    return isinstance(thing, UnionType) or get_origin(thing) is typing.Union


def is_a_type(thing):
    """Return True if thing is a type or a generic type like thing."""
    return isinstance(thing, type) or is_generic_type(thing) or is_a_new_type(thing)


def is_typing_literal(thing):
    return get_origin(thing) in (
        typing.Literal,
        getattr(typing_extensions, "Literal", object()),
    )


def is_annotated_type(thing):
    return (
        isinstance(thing, _AnnotatedAlias)
        and getattr(thing, "__args__", None) is not None
    )


def get_constraints_filter_map():
    if at := sys.modules.get("annotated_types"):
        return {
            # Due to the order of operator.gt/ge/lt/le arguments, order is inversed:
            at.Gt: lambda constraint: partial(operator.lt, constraint.gt),
            at.Ge: lambda constraint: partial(operator.le, constraint.ge),
            at.Lt: lambda constraint: partial(operator.gt, constraint.lt),
            at.Le: lambda constraint: partial(operator.ge, constraint.le),
            at.MinLen: lambda constraint: partial(min_len, constraint.min_length),
            at.MaxLen: lambda constraint: partial(max_len, constraint.max_length),
            at.Predicate: lambda constraint: constraint.func,
        }
    return {}  # pragma: no cover


def _get_constraints(args: Tuple[Any, ...]) -> Iterator["at.BaseMetadata"]:
    if at := sys.modules.get("annotated_types"):
        for arg in args:
            if isinstance(arg, at.BaseMetadata):
                yield arg
            elif getattr(arg, "__is_annotated_types_grouped_metadata__", False):
                yield from arg
            elif isinstance(arg, slice) and arg.step in (1, None):
                yield from at.Len(arg.start or 0, arg.stop)


def _flat_annotated_repr_parts(annotated_type):
    # Helper to get a good error message in find_annotated_strategy() below.
    type_reps = [
        get_pretty_function_description(a)
        for a in annotated_type.__args__
        if not isinstance(a, typing.TypeVar)
    ]
    metadata_reps = []
    for m in getattr(annotated_type, "__metadata__", ()):
        if is_annotated_type(m):
            ts, ms = _flat_annotated_repr_parts(m)
            type_reps.extend(ts)
            metadata_reps.extend(ms)
        else:
            metadata_reps.append(get_pretty_function_description(m))
    return type_reps, metadata_reps


def find_annotated_strategy(annotated_type):
    metadata = getattr(annotated_type, "__metadata__", ())

    if any(is_annotated_type(arg) for arg in metadata):
        # Annotated[Annotated[T], ...] is perfectly acceptable, but it's all to easy
        # to instead write Annotated[T1, Annotated[T2, ...]] - and nobody else checks
        # for that at runtime.  Once you add generics this can be seriously confusing,
        # so we go to some trouble to give a helpful error message.
        # For details: https://github.com/HypothesisWorks/hypothesis/issues/3891
        ty_rep = repr(annotated_type).replace("typing.Annotated", "Annotated")
        ts, ms = _flat_annotated_repr_parts(annotated_type)
        bits = ", ".join([" | ".join(dict.fromkeys(ts or "?")), *dict.fromkeys(ms)])
        raise ResolutionFailed(
            f"`{ty_rep}` is invalid because nesting Annotated is only allowed for "
            f"the first (type) argument, not for later (metadata) arguments.  "
            f"Did you mean `Annotated[{bits}]`?"
        )
    for arg in reversed(metadata):
        if isinstance(arg, st.SearchStrategy):
            return arg

    filter_conditions = []
    if "annotated_types" in sys.modules:
        unsupported = []
        for constraint in _get_constraints(metadata):
            if convert := get_constraints_filter_map().get(type(constraint)):
                filter_conditions.append(convert(constraint))
            else:
                unsupported.append(constraint)
        if unsupported:
            msg = f"Ignoring unsupported {', '.join(map(repr, unsupported))}"
            warnings.warn(msg, HypothesisWarning, stacklevel=2)

    base_strategy = st.from_type(annotated_type.__origin__)
    for filter_condition in filter_conditions:
        base_strategy = base_strategy.filter(filter_condition)

    return base_strategy


def has_type_arguments(type_):
    """Decides whethere or not this type has applied type arguments."""
    args = getattr(type_, "__args__", None)
    if args and isinstance(type_, (typing._GenericAlias, GenericAlias)):
        # There are some cases when declared types do already have type arguments
        # Like `Sequence`, that is `_GenericAlias(abc.Sequence[T])[T]`
        parameters = getattr(type_, "__parameters__", None)
        if parameters:  # So, we need to know if type args are just "aliases"
            return args != parameters
    return bool(args)


def is_generic_type(type_):
    """Decides whether a given type is generic or not."""
    # The ugly truth is that `MyClass`, `MyClass[T]`, and `MyClass[int]` are very different.
    # We check for `MyClass[T]` and `MyClass[int]` with the first condition,
    # while the second condition is for `MyClass`.
    return isinstance(type_, (*typing_root_type, GenericAlias)) or (
        isinstance(type_, type)
        and (typing.Generic in type_.__mro__ or hasattr(type_, "__class_getitem__"))
    )


def _try_import_forward_ref(thing, bound):  # pragma: no cover
    """
    Tries to import a real bound type from ``TypeVar`` bound to a ``ForwardRef``.

    This function is very "magical" to say the least, please don't use it.
    This function fully covered, but is excluded from coverage
    because we can only cover each path in a separate python version.
    """
    try:
        return typing._eval_type(bound, vars(sys.modules[thing.__module__]), None)
    except (KeyError, AttributeError, NameError):
        # We fallback to `ForwardRef` instance, you can register it as a type as well:
        # >>> from typing import ForwardRef
        # >>> from hypothesis import strategies as st
        # >>> st.register_type_strategy(ForwardRef('YourType'), your_strategy)
        return bound


def from_typing_type(thing):
    # We start with Final, Literal, and Annotated since they don't support `isinstance`.
    #
    # We then explicitly error on non-Generic types, which don't carry enough
    # information to sensibly resolve to strategies at runtime.
    # Finally, we run a variation of the subclass lookup in `st.from_type`
    # among generic types in the lookup.
    if get_origin(thing) == typing.Final:
        return st.one_of([st.from_type(t) for t in thing.__args__])
    if is_typing_literal(thing):
        args_dfs_stack = list(thing.__args__)
        literals = []
        while args_dfs_stack:
            arg = args_dfs_stack.pop()
            if is_typing_literal(arg):  # pragma: no cover
                # Python 3.10+ flattens for us when constructing Literal objects
                args_dfs_stack.extend(reversed(arg.__args__))
            else:
                literals.append(arg)
        return st.sampled_from(literals)
    if is_annotated_type(thing):  # pragma: no cover
        # This requires Python 3.9+ or the typing_extensions package
        annotated_strategy = find_annotated_strategy(thing)
        if annotated_strategy is not None:
            return annotated_strategy
        args = thing.__args__
        assert args, "it's impossible to make an annotated type with no args"
        annotated_type = args[0]
        return st.from_type(annotated_type)
    # Now, confirm that we're dealing with a generic type as we expected
    if sys.version_info[:2] < (3, 9) and not isinstance(
        thing, typing_root_type
    ):  # pragma: no cover
        raise ResolutionFailed(f"Cannot resolve {thing} to a strategy")

    # Some "generic" classes are not generic *in* anything - for example both
    # Hashable and Sized have `__args__ == ()`
    origin = get_origin(thing) or thing
    if (
        origin in vars(collections.abc).values()
        and len(getattr(thing, "__args__", None) or []) == 0
    ):
        return st.from_type(origin)

    # Parametrised generic types have their __origin__ attribute set to the
    # un-parametrised version, which we need to use in the subclass checks.
    # e.g.:     typing.List[int].__origin__ == typing.List
    # (actually not sure if this is true since Python 3.9 or so)
    mapping = {
        k: v
        for k, v in _global_type_lookup.items()
        if is_generic_type(k) and try_issubclass(k, thing)
    }
    # Drop some unusual cases for simplicity, including tuples or its
    # subclasses (e.g. namedtuple)
    if len(mapping) > 1:
        _Environ = getattr(os, "_Environ", None)
        mapping.pop(_Environ, None)
    tuple_types = [
        t
        for t in mapping
        if (isinstance(t, type) and issubclass(t, tuple)) or t is typing.Tuple
    ]
    if len(mapping) > len(tuple_types):
        for tuple_type in tuple_types:
            mapping.pop(tuple_type)

    # After we drop Python 3.8 and can rely on having generic builtin types, we'll
    # be able to simplify this logic by dropping the typing-module handling.
    if {dict, set, typing.Dict, typing.Set}.intersection(mapping):
        # ItemsView can cause test_lookup.py::test_specialised_collection_types
        # to fail, due to weird isinstance behaviour around the elements.
        mapping.pop(collections.abc.ItemsView, None)
        mapping.pop(typing.ItemsView, None)
    if {collections.deque, typing.Deque}.intersection(mapping) and len(mapping) > 1:
        # Resolving generic sequences to include a deque is more trouble for e.g.
        # the ghostwriter than it's worth, via undefined names in the repr.
        mapping.pop(collections.deque, None)
        mapping.pop(typing.Deque, None)

    if len(mapping) > 1:
        # issubclass treats bytestring as a kind of sequence, which it is,
        # but treating it as such breaks everything else when it is presumed
        # to be a generic sequence or container that could hold any item.
        # Except for sequences of integers, or unions which include integer!
        # See https://github.com/HypothesisWorks/hypothesis/issues/2257
        #
        # This block drops bytes from the types that can be generated
        # if there is more than one allowed type, and the element type is
        # not either `int` or a Union with `int` as one of its elements.
        elem_type = (getattr(thing, "__args__", None) or ["not int"])[0]
        if is_a_union(elem_type):
            union_elems = elem_type.__args__
        else:
            union_elems = ()
        if not any(
            isinstance(T, type) and issubclass(int, get_origin(T) or T)
            for T in [*union_elems, elem_type]
        ):
            mapping.pop(bytes, None)
            mapping.pop(collections.abc.ByteString, None)
            mapping.pop(typing.ByteString, None)
    elif (
        (not mapping)
        and isinstance(thing, typing.ForwardRef)
        and thing.__forward_arg__ in vars(builtins)
    ):
        return st.from_type(getattr(builtins, thing.__forward_arg__))
    # Before Python 3.9, we sometimes have e.g. Sequence from both the typing
    # module, and collections.abc module.  Discard any type which is not it's own
    # origin, where the origin is also in the mapping.
    for t in sorted(mapping, key=type_sorting_key):
        origin = get_origin(t)
        if origin is not t and origin in mapping:
            mapping.pop(t)
    # Sort strategies according to our type-sorting heuristic for stable output
    strategies = [
        s
        for s in (
            v if isinstance(v, st.SearchStrategy) else v(thing)
            for k, v in sorted(mapping.items(), key=lambda kv: type_sorting_key(kv[0]))
            if sum(try_issubclass(k, T) for T in mapping) == 1
        )
        if s != NotImplemented
    ]
    empty = ", ".join(repr(s) for s in strategies if s.is_empty)
    if empty or not strategies:
        raise ResolutionFailed(
            f"Could not resolve {empty or thing} to a strategy; "
            "consider using register_type_strategy"
        )
    return st.one_of(strategies)


def can_cast(type, value):
    """Determine if value can be cast to type."""
    try:
        type(value)
        return True
    except Exception:
        return False


def _networks(bits):
    return st.tuples(st.integers(0, 2**bits - 1), st.integers(-bits, 0).map(abs))


utc_offsets = st.builds(
    datetime.timedelta, minutes=st.integers(0, 59), hours=st.integers(-23, 23)
)

# These builtin and standard-library types have Hypothesis strategies,
# seem likely to appear in type annotations, or are otherwise notable.
#
# The strategies below must cover all possible values from the type, because
# many users treat them as comprehensive and one of Hypothesis' design goals
# is to avoid testing less than expected.
#
# As a general rule, we try to limit this to scalars because from_type()
# would have to decide on arbitrary collection elements, and we'd rather
# not (with typing module generic types and some builtins as exceptions).
#
# Strategy Callables may return NotImplemented, which should be treated in the
# same way as if the type was not registered.
#
# Note that NotImplemented cannot be typed in Python 3.8 because there's no type
# exposed for it, and NotImplemented itself is typed as Any so that it can be
# returned without being listed in a function signature:
# https://github.com/python/mypy/issues/6710#issuecomment-485580032
_global_type_lookup: typing.Dict[
    type, typing.Union[st.SearchStrategy, typing.Callable[[type], st.SearchStrategy]]
] = {
    type(None): st.none(),
    bool: st.booleans(),
    int: st.integers(),
    float: st.floats(),
    complex: st.complex_numbers(),
    fractions.Fraction: st.fractions(),
    decimal.Decimal: st.decimals(),
    str: st.text(),
    bytes: st.binary(),
    datetime.datetime: st.datetimes(),
    datetime.date: st.dates(),
    datetime.time: st.times(),
    datetime.timedelta: st.timedeltas(),
    datetime.timezone: st.builds(datetime.timezone, offset=utc_offsets)
    | st.builds(datetime.timezone, offset=utc_offsets, name=st.text(st.characters())),
    uuid.UUID: st.uuids(),
    tuple: st.builds(tuple),
    list: st.builds(list),
    set: st.builds(set),
    collections.abc.MutableSet: st.builds(set),
    frozenset: st.builds(frozenset),
    dict: st.builds(dict),
    FunctionType: st.functions(),
    type(Ellipsis): st.just(Ellipsis),
    type(NotImplemented): st.just(NotImplemented),
    bytearray: st.binary().map(bytearray),
    memoryview: st.binary().map(memoryview),
    numbers.Real: st.floats(),
    numbers.Rational: st.fractions(),
    numbers.Number: st.complex_numbers(),
    numbers.Integral: st.integers(),
    numbers.Complex: st.complex_numbers(),
    slice: st.builds(
        slice,
        st.none() | st.integers(),
        st.none() | st.integers(),
        st.none() | st.integers(),
    ),
    range: st.one_of(
        st.builds(range, st.integers(min_value=0)),
        st.builds(range, st.integers(), st.integers()),
        st.builds(range, st.integers(), st.integers(), st.integers().filter(bool)),
    ),
    ipaddress.IPv4Address: ip_addresses(v=4),
    ipaddress.IPv6Address: ip_addresses(v=6),
    ipaddress.IPv4Interface: _networks(32).map(ipaddress.IPv4Interface),
    ipaddress.IPv6Interface: _networks(128).map(ipaddress.IPv6Interface),
    ipaddress.IPv4Network: st.one_of(
        _networks(32).map(lambda x: ipaddress.IPv4Network(x, strict=False)),
        st.sampled_from(SPECIAL_IPv4_RANGES).map(ipaddress.IPv4Network),
    ),
    ipaddress.IPv6Network: st.one_of(
        _networks(128).map(lambda x: ipaddress.IPv6Network(x, strict=False)),
        st.sampled_from(SPECIAL_IPv6_RANGES).map(ipaddress.IPv6Network),
    ),
    os.PathLike: st.builds(PurePath, st.text()),
    UnicodeDecodeError: st.builds(
        UnicodeDecodeError,
        st.just("unknown encoding"),
        st.just(b""),
        st.just(0),
        st.just(0),
        st.just("reason"),
    ),
    UnicodeEncodeError: st.builds(
        UnicodeEncodeError,
        st.just("unknown encoding"),
        st.text(),
        st.just(0),
        st.just(0),
        st.just("reason"),
    ),
    UnicodeTranslateError: st.builds(
        UnicodeTranslateError, st.text(), st.just(0), st.just(0), st.just("reason")
    ),
    BaseExceptionGroup: st.builds(
        BaseExceptionGroup,
        st.text(),
        st.lists(st.from_type(BaseException), min_size=1, max_size=5),
    ),
    ExceptionGroup: st.builds(
        ExceptionGroup,
        st.text(),
        st.lists(st.from_type(Exception), min_size=1, max_size=5),
    ),
    enumerate: st.builds(enumerate, st.just(())),
    filter: st.builds(filter, st.just(lambda _: None), st.just(())),
    map: st.builds(map, st.just(lambda _: None), st.just(())),
    reversed: st.builds(reversed, st.just(())),
    zip: st.builds(zip),  # avoids warnings on PyPy 7.3.14+
    property: st.builds(property, st.just(lambda _: None)),
    classmethod: st.builds(classmethod, st.just(lambda self: self)),
    staticmethod: st.builds(staticmethod, st.just(lambda self: self)),
    super: st.builds(super, st.from_type(type)),
    re.Match: st.text().map(lambda c: re.match(".", c, flags=re.DOTALL)).filter(bool),
    re.Pattern: st.builds(re.compile, st.sampled_from(["", b""])),
    random.Random: st.randoms(),
    # Pull requests with more types welcome!
}
if zoneinfo is not None:  # pragma: no branch
    _global_type_lookup[zoneinfo.ZoneInfo] = st.timezones()
if PYPY:
    _global_type_lookup[builtins.sequenceiterator] = st.builds(iter, st.tuples())  # type: ignore


_global_type_lookup[type] = st.sampled_from(
    [type(None), *sorted(_global_type_lookup, key=str)]
)
if sys.version_info[:2] >= (3, 9):
    # subclass of MutableMapping, and in Python 3.9 we resolve to a union
    # which includes this... but we don't actually ever want to build one.
    _global_type_lookup[os._Environ] = st.just(os.environ)


_global_type_lookup.update(
    {
        # Note: while ByteString notionally also represents the bytearray and
        # memoryview types, it is a subclass of Hashable and those types are not.
        # We therefore only generate the bytes type. type-ignored due to deprecation.
        typing.ByteString: st.binary(),  # type: ignore
        collections.abc.ByteString: st.binary(),  # type: ignore
        # TODO: SupportsAbs and SupportsRound should be covariant, ie have functions.
        typing.SupportsAbs: st.one_of(
            st.booleans(),
            st.integers(),
            st.floats(),
            st.complex_numbers(),
            st.fractions(),
            st.decimals(),
            st.timedeltas(),
        ),
        typing.SupportsRound: st.one_of(
            st.booleans(), st.integers(), st.floats(), st.decimals(), st.fractions()
        ),
        typing.SupportsComplex: st.one_of(
            st.booleans(),
            st.integers(),
            st.floats(),
            st.complex_numbers(),
            st.decimals(),
            st.fractions(),
        ),
        typing.SupportsFloat: st.one_of(
            st.booleans(),
            st.integers(),
            st.floats(),
            st.decimals(),
            st.fractions(),
            # with floats its far more annoying to capture all
            # the magic in a regex. so we just stringify some floats
            st.floats().map(str),
        ),
        typing.SupportsInt: st.one_of(
            st.booleans(),
            st.integers(),
            st.floats(),
            st.uuids(),
            st.decimals(),
            # this generates strings that should able to be parsed into integers
            st.from_regex(r"\A-?\d+\Z").filter(functools.partial(can_cast, int)),
        ),
        typing.SupportsIndex: st.integers() | st.booleans(),
        typing.SupportsBytes: st.one_of(
            st.booleans(),
            st.binary(),
            st.integers(0, 255),
            # As with Reversible, we tuplize this for compatibility with Hashable.
            st.lists(st.integers(0, 255)).map(tuple),
        ),
        typing.BinaryIO: st.builds(io.BytesIO, st.binary()),
        typing.TextIO: st.builds(io.StringIO, st.text()),
    }
)


# The "extra" lookups define a callable that either resolves to a strategy for
# this narrowly extra-specific type, or returns None to proceed with normal
# type resolution. The callable will only be called if the module is
# installed. To avoid the performance hit of importing anything here, we defer
# it until the method is called the first time, at which point we replace the
# entry in the lookup table with the direct call.
def _from_numpy_type(thing: typing.Type) -> typing.Optional[st.SearchStrategy]:
    from hypothesis.extra.numpy import _from_type

    _global_extra_lookup["numpy"] = _from_type
    return _from_type(thing)


_global_extra_lookup: typing.Dict[
    str, typing.Callable[[typing.Type], typing.Optional[st.SearchStrategy]]
] = {
    "numpy": _from_numpy_type,
}


def register(type_, fallback=None, *, module=typing):
    if isinstance(type_, str):
        # Use the name of generic types which are not available on all
        # versions, and the function just won't be added to the registry
        type_ = getattr(module, type_, None)
        if type_ is None:  # pragma: no cover
            return lambda f: f

    def inner(func):
        nonlocal type_
        if fallback is None:
            _global_type_lookup[type_] = func
            return func

        @functools.wraps(func)
        def really_inner(thing):
            # This branch is for Python <= 3.8, when __args__ was not always tracked
            if getattr(thing, "__args__", None) is None:
                return fallback  # pragma: no cover
            return func(thing)

        if sys.version_info[:2] >= (3, 9):
            try:
                type_ = get_origin(type_)
            except Exception:
                pass
        _global_type_lookup[type_] = really_inner
        return really_inner

    return inner


@register(typing.Type)
@register("Type", module=typing_extensions)
def resolve_Type(thing):
    if getattr(thing, "__args__", None) is None:
        # This branch is for Python <= 3.8, when __args__ was not always tracked
        return st.just(type)  # pragma: no cover
    args = (thing.__args__[0],)
    if is_a_union(args[0]):
        args = args[0].__args__
    # Duplicate check from from_type here - only paying when needed.
    args = list(args)
    for i, a in enumerate(args):
        if type(a) == typing.ForwardRef:
            try:
                args[i] = getattr(builtins, a.__forward_arg__)
            except AttributeError:
                raise ResolutionFailed(
                    f"Cannot find the type referenced by {thing} - try using "
                    f"st.register_type_strategy({thing}, st.from_type(...))"
                ) from None
    return st.sampled_from(sorted(args, key=type_sorting_key))


@register(typing.List, st.builds(list))
def resolve_List(thing):
    return st.lists(st.from_type(thing.__args__[0]))


@register(typing.Tuple, st.builds(tuple))
def resolve_Tuple(thing):
    elem_types = getattr(thing, "__args__", None) or ()
    if len(elem_types) == 2 and elem_types[-1] is Ellipsis:
        return st.lists(st.from_type(elem_types[0])).map(tuple)
    elif len(elem_types) == 1 and elem_types[0] == ():
        return st.tuples()  # Empty tuple; see issue #1583
    return st.tuples(*map(st.from_type, elem_types))


def _can_hash(val):
    try:
        hash(val)
        return True
    except Exception:
        return False


# Some types are subclasses of typing.Hashable, because they define a __hash__
# method, but have non-hashable instances such as `Decimal("snan")` or may contain
# such instances (e.g. `FrozenSet[Decimal]`).  We therefore keep this whitelist of
# types which are always hashable, and apply the `_can_hash` filter to all others.
# Our goal is not completeness, it's to get a small performance boost for the most
# common cases, and a short whitelist is basically free to maintain.
ALWAYS_HASHABLE_TYPES = {type(None), bool, int, float, complex, str, bytes}


def _from_hashable_type(type_):
    if type_ in ALWAYS_HASHABLE_TYPES:
        return st.from_type(type_)
    else:
        return st.from_type(type_).filter(_can_hash)


@register(typing.Set, st.builds(set))
@register(typing.MutableSet, st.builds(set))
def resolve_Set(thing):
    return st.sets(_from_hashable_type(thing.__args__[0]))


@register(typing.FrozenSet, st.builds(frozenset))
def resolve_FrozenSet(thing):
    return st.frozensets(_from_hashable_type(thing.__args__[0]))


@register(typing.Dict, st.builds(dict))
def resolve_Dict(thing):
    # If thing is a Collection instance, we need to fill in the values
    keys_vals = thing.__args__ * 2
    return st.dictionaries(
        _from_hashable_type(keys_vals[0]), st.from_type(keys_vals[1])
    )


@register(typing.DefaultDict, st.builds(collections.defaultdict))
@register("DefaultDict", st.builds(collections.defaultdict), module=typing_extensions)
def resolve_DefaultDict(thing):
    return resolve_Dict(thing).map(lambda d: collections.defaultdict(None, d))


@register(typing.ItemsView, st.builds(dict).map(dict.items))
def resolve_ItemsView(thing):
    return resolve_Dict(thing).map(dict.items)


@register(typing.KeysView, st.builds(dict).map(dict.keys))
def resolve_KeysView(thing):
    return st.dictionaries(_from_hashable_type(thing.__args__[0]), st.none()).map(
        dict.keys
    )


@register(typing.ValuesView, st.builds(dict).map(dict.values))
def resolve_ValuesView(thing):
    return st.dictionaries(st.integers(), st.from_type(thing.__args__[0])).map(
        dict.values
    )


@register(typing.Iterator, st.iterables(st.nothing()))
def resolve_Iterator(thing):
    return st.iterables(st.from_type(thing.__args__[0]))


@register(typing.Counter, st.builds(collections.Counter))
def resolve_Counter(thing):
    return st.dictionaries(
        keys=st.from_type(thing.__args__[0]),
        values=st.integers(),
    ).map(collections.Counter)


@register(typing.Deque, st.builds(collections.deque))
def resolve_deque(thing):
    return st.lists(st.from_type(thing.__args__[0])).map(collections.deque)


@register(typing.ChainMap, st.builds(dict).map(collections.ChainMap))
def resolve_ChainMap(thing):
    return resolve_Dict(thing).map(collections.ChainMap)


@register(typing.OrderedDict, st.builds(dict).map(collections.OrderedDict))
def resolve_OrderedDict(thing):
    return resolve_Dict(thing).map(collections.OrderedDict)


@register(typing.Pattern, st.builds(re.compile, st.sampled_from(["", b""])))
def resolve_Pattern(thing):
    if isinstance(thing.__args__[0], typing.TypeVar):  # pragma: no cover
        # TODO: this was covered on Python 3.8, but isn't on 3.10 - we should
        # work out why not and write some extra tests to help avoid regressions.
        return st.builds(re.compile, st.sampled_from(["", b""]))
    return st.just(re.compile(thing.__args__[0]()))


@register(  # pragma: no branch  # coverage does not see lambda->exit branch
    typing.Match,
    st.text().map(lambda c: re.match(".", c, flags=re.DOTALL)).filter(bool),
)
def resolve_Match(thing):
    if thing.__args__[0] == bytes:
        return (
            st.binary(min_size=1)
            .map(lambda c: re.match(b".", c, flags=re.DOTALL))
            .filter(bool)
        )
    return st.text().map(lambda c: re.match(".", c, flags=re.DOTALL)).filter(bool)


class GeneratorStrategy(st.SearchStrategy):
    def __init__(self, yields, returns):
        assert isinstance(yields, st.SearchStrategy)
        assert isinstance(returns, st.SearchStrategy)
        self.yields = yields
        self.returns = returns

    def __repr__(self):
        return f"<generators yields={self.yields!r} returns={self.returns!r}>"

    def do_draw(self, data):
        elements = conjecture_utils_many(data, min_size=0, max_size=100, average_size=5)
        while elements.more():
            yield data.draw(self.yields)
        return data.draw(self.returns)


@register(typing.Generator, GeneratorStrategy(st.none(), st.none()))
def resolve_Generator(thing):
    yields, _, returns = thing.__args__
    return GeneratorStrategy(st.from_type(yields), st.from_type(returns))


@register(typing.Callable, st.functions())
def resolve_Callable(thing):
    # Generated functions either accept no arguments, or arbitrary arguments.
    # This is looser than ideal, but anything tighter would generally break
    # use of keyword arguments and we'd rather not force positional-only.
    if not thing.__args__:  # pragma: no cover  # varies by minor version
        return st.functions()

    *args_types, return_type = thing.__args__

    # Note that a list can only appear in __args__ under Python 3.9 with the
    # collections.abc version; see https://bugs.python.org/issue42195
    if len(args_types) == 1 and isinstance(args_types[0], list):
        args_types = tuple(args_types[0])  # pragma: no cover

    pep612 = ConcatenateTypes + ParamSpecTypes
    for arg in args_types:
        # awkward dance because you can't use Concatenate in isistance or issubclass
        if getattr(arg, "__origin__", arg) in pep612 or type(arg) in pep612:
            raise InvalidArgument(
                "Hypothesis can't yet construct a strategy for instances of a "
                f"Callable type parametrized by {arg!r}.  Consider using an "
                "explicit strategy, or opening an issue."
            )
    if get_origin(return_type) in TypeGuardTypes:
        raise InvalidArgument(
            "Hypothesis cannot yet construct a strategy for callables which "
            f"are PEP-647 TypeGuards (got {return_type!r}).  "
            "Consider using an explicit strategy, or opening an issue."
        )

    return st.functions(
        like=(lambda *a, **k: None) if args_types else (lambda: None),
        returns=st.from_type(return_type),
    )


@register(typing.TypeVar)
def resolve_TypeVar(thing):
    type_var_key = f"typevar={thing!r}"

    if getattr(thing, "__bound__", None) is not None:
        bound = thing.__bound__
        if isinstance(bound, typing.ForwardRef):
            bound = _try_import_forward_ref(thing, bound)
        strat = unwrap_strategies(st.from_type(bound))
        if not isinstance(strat, OneOfStrategy):
            return strat
        # The bound was a union, or we resolved it as a union of subtypes,
        # so we need to unpack the strategy to ensure consistency across uses.
        # This incantation runs a sampled_from over the strategies inferred for
        # each part of the union, wraps that in shared so that we only generate
        # from one type per testcase, and flatmaps that back to instances.
        return st.shared(
            st.sampled_from(strat.original_strategies), key=type_var_key
        ).flatmap(lambda s: s)

    builtin_scalar_types = [type(None), bool, int, float, str, bytes]
    return st.shared(
        st.sampled_from(
            # Constraints may be None or () on various Python versions.
            getattr(thing, "__constraints__", None)
            or builtin_scalar_types,
        ),
        key=type_var_key,
    ).flatmap(st.from_type)
