#!/usr/bin/env python3
# encoding: utf-8

__author__ = "ChenyangGao <https://chenyanggao.github.io>"
__version__ = (0, 0, 2)
__all__ = [
    "as_thread", "ensure_async", "ensure_await", "ensure_coroutine", "ensure_aiter", 
    "async_map", "async_filter", "async_reduce", "async_zip", "call_as_aiter", "to_list", 
]

from asyncio import to_thread
from collections.abc import Awaitable, AsyncIterable, AsyncIterator, Callable, Coroutine, Iterable
from inspect import isawaitable, iscoroutinefunction, isgenerator
from typing import cast, Any, ParamSpec, TypeVar

from decotools import decorated
from undefined import undefined


Args = ParamSpec("Args")
T = TypeVar("T")


@decorated
def as_thread(func: Callable[Args, T], /, *args, **kwds) -> Awaitable[T]:
    def wrapfunc(*args, **kwds):
        try:
            return func(*args, **kwds)
        except StopIteration as e:
            raise StopAsyncIteration from e
    return to_thread(wrapfunc, *args, **kwds)


def ensure_async(
    func: Callable[Args, T | Awaitable[T]], 
    /, 
    threaded: bool = True, 
) -> Callable[Args, Awaitable[T]]:
    if iscoroutinefunction(func):
        return func
    func = cast(Callable[Args, T], func)
    if threaded:
        func = as_thread(func)
        async def wrapper(*args, **kwds):
            ret = await func(*args, **kwds)
            if isawaitable(ret):
                try:
                    return await ret
                except StopIteration as e:
                    raise StopAsyncIteration from e
            return ret
    else:
        async def wrapper(*args, **kwds):
            try:
                ret = func(*args, **kwds)
                if isawaitable(ret):
                    return await ret
                return ret
            except StopIteration as e:
                raise StopAsyncIteration from e
    return wrapper


def ensure_await(o, /) -> Awaitable:
    if isawaitable(o):
        return o
    async def wrapper():
        return o
    return wrapper()


def ensure_coroutine(o, /) -> Coroutine:
    async def wrapper():
        if isawaitable(o):
            return await o
        return o
    return wrapper()


def ensure_aiter(
    it: Iterable[T] | AsyncIterable[T], 
    /, 
    threaded: bool = True, 
) -> AsyncIterator[T]:
    if isinstance(it, AsyncIterable):
        return aiter(it)
    if isgenerator(it):
        send = ensure_async(it.send, threaded=threaded)
        async def wrapper():
            e: Any = None
            try:
                while True:
                    e = yield await send(e)
            except StopAsyncIteration:
                pass
    else:
        get = ensure_async(iter(it).__next__, threaded=threaded)
        async def wrapper():
            try:
                while True:
                    yield await get()
            except:
                pass
    return wrapper()


async def async_map(func, iterable, /, *iterables, threaded: bool = True):
    func = ensure_async(func, threaded=threaded)
    if iterables:
        async for args in async_zip(iterable, *iterables, threaded=threaded):
            yield await func(*args)
    else:
        async for arg in ensure_aiter(iterable, threaded=threaded):
            yield await func(arg)


async def async_filter(func, iterable, /, threaded: bool = True):
    func = ensure_async(func, threaded=threaded)
    async for arg in ensure_aiter(iterable, threaded=threaded):
        if (await func(arg)):
            yield arg


async def async_reduce(func, iterable, initial=undefined, /, threaded: bool = True):
    ait = ensure_aiter(iterable, threaded=threaded)
    if initial is undefined:
        try:
            initial = await ait.__anext__()
        except StopAsyncIteration:
            raise TypeError("reduce() of empty iterable with no initial value")
    func = ensure_async(func, threaded=threaded)
    prev = initial
    async for arg in ait:
        prev = await func(prev, arg)
    return prev


async def async_zip(iterable, /, *iterables, threaded: bool = True):
    iterable = ensure_aiter(iterable, threaded=threaded)
    if iterables:
        fs = (iterable.__anext__, *(ensure_aiter(it, threaded=threaded).__anext__ for it in iterables))
        try:
            while True:
                yield tuple([await f() for f in fs])
        except StopAsyncIteration:
            pass
    else:
        async for e in iterable:
            yield e


async def call_as_aiter(
    func: Callable[[], T] | Callable[[], Awaitable[T]], 
    /, 
    sentinel = undefined, 
    threaded: bool = True, 
) -> AsyncIterator[T]:
    func = ensure_async(func, threaded=threaded)
    try:
        if sentinel is undefined:
            while True:
                yield await func()
        elif callable(sentinel):
            sentinel = ensure_async(sentinel)
            while not (await sentinel(r := await func())):
                yield r
        else:
            check = lambda r, /: r is not sentinel and r != sentinel
            while check(r := await func()):
                yield r
    except (StopIteration, StopAsyncIteration):
        pass


async def to_list(it: Iterable[T] | AsyncIterable[T], /) -> list[T]:
    return [e async for e in ensure_aiter(it)]

