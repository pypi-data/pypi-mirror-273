#!/usr/bin/env python3
# encoding: utf-8

__author__ = "ChenyangGao <https://chenyanggao.github.io>"
__version__ = (0, 0, 1)
__all__ = ["iterable", "async_iterable", "acc_step", "cut_iter", "asyncify_iter"]

from asyncio import to_thread
from collections.abc import AsyncGenerator, AsyncIterable, Generator, Iterable, Iterator
from typing import overload, Any, Optional, TypeVar


TI = TypeVar("TI")
TO = TypeVar("TO")


def iterable(it, /) -> bool:
    try:
        return isinstance(iter(it), Iterable)
    except TypeError:
        return False


def async_iterable(it, /) -> bool:
    try:
        return isinstance(iter(it), AsyncIterable)
    except TypeError:
        return False


def acc_step(
    start: int, 
    stop: Optional[int] = None, 
    step: int = 1, 
) -> Iterator[tuple[int, int, int]]:
    if stop is None:
        start, stop = 0, start
    for i in range(start + step, stop, step):
        yield start, (start := i), step
    if start != stop:
        yield start, stop, stop - start


def cut_iter(
    start: int, 
    stop: Optional[int] = None, 
    step: int = 1, 
) -> Iterator[tuple[int, int]]:
    if stop is None:
        start, stop = 0, start
    for start in range(start + step, stop, step):
        yield start, step
    if start != stop:
        yield stop, stop - start


@overload
async def _asyncify_iter(it: Generator[TI, TO, Any], /, wait_for_thread: bool) -> AsyncGenerator[TI, TO]: ...
@overload
async def _asyncify_iter(it: Iterable[TO], /, wait_for_thread: bool) -> AsyncGenerator[Any, TO]: ...
async def _asyncify_iter(it, /, wait_for_thread: bool = False):
    if wait_for_thread:
        if isinstance(it, Generator):
            send = it.send
            def nextval(val):
                try:
                    return send(val), None
                except BaseException as e:
                    return None, e
        else:
            getnext = iter(it).__next__
            def nextval(val):
                try:
                    return getnext(), None
                except BaseException as e:
                    return None, e
        val = None
        while True:
            yield_val, exc = await to_thread(nextval, val)
            if exc is None:
                yield yield_val
            elif isinstance(exc, StopIteration):
                break
            else:
                raise exc
    elif isinstance(it, Generator):
        send = it.send
        val = None
        try:
            while True:
                val = yield send(val)
        except StopIteration:
            pass
    else:
        for val in it:
            yield val


@overload
def asyncify_iter(it: AsyncIterable[TO], /, wait_for_thread: bool) -> AsyncIterable[TO]: ...
@overload
def asyncify_iter(it: Generator[TI, TO, Any], /, wait_for_thread: bool) -> AsyncGenerator[TI, TO]: ...
@overload
def asyncify_iter(it: Iterable[TO], /, wait_for_thread: bool) -> AsyncGenerator[Any, TO]: ...
def asyncify_iter(it, /, wait_for_thread: bool = False):
    if isinstance(it, AsyncIterable):
        return it
    return _asyncify_iter(it, wait_for_thread=wait_for_thread)

