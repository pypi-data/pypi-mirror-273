from asyncio import Lock
from datetime import timedelta
from functools import wraps
from inspect import iscoroutinefunction
from threading import RLock
import time
from typing import (
    Any,
    Callable,
    cast,
    Counter,
    ItemsView,
    Iterator,
    KeysView,
    MutableMapping,
    OrderedDict,
    overload,
    ParamSpec,
    TypeVar,
    ValuesView,
)

P = ParamSpec("P")
R = TypeVar("R")

T = TypeVar("T")
TD = TypeVar("TD")

HashFunc = Callable[..., tuple[Any, ...]]

_undefined = object()


class Cache(MutableMapping[str, T]):
    def __init__(self) -> None:
        self._data: OrderedDict[str, T] = OrderedDict()

    def __getitem__(self, key: str) -> T:
        return self._data[key]

    def __setitem__(self, key: str, value: T) -> None:
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def keys(self) -> KeysView[str]:
        return self._data.keys()

    def values(self) -> ValuesView[T]:
        return self._data.values()

    def items(self) -> ItemsView[str, T]:
        return self._data.items()

    @overload
    def get(self, key: str) -> T | None:
        ...

    @overload
    def get(self, key: str, default: T) -> T:
        ...

    def get(self, key: str, default: T | None = None) -> T | None:
        try:
            return self[key]
        except KeyError:
            return default

    @overload
    def pop(self, key: str) -> T:
        ...

    @overload
    def pop(self, key: str, default: TD) -> T | TD:
        ...

    def pop(self, key: str, default: Any = _undefined) -> Any:
        if default is not _undefined:
            return self._data.pop(key, default)
        return self._data.pop(key)

    def popitem(self) -> tuple[str, T]:
        return self._data.popitem()

    def setdefault(self, key: str, default: T) -> T:
        try:
            return self[key]
        except KeyError:
            self[key] = default
            return default

    def clear(self) -> None:
        self._data.clear()

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __data_repr__(self) -> dict[str, T]:
        return dict(self._data)


class FIFOCache(Cache[T]):
    def __init__(self, maxsize: int = 256) -> None:
        super().__init__()
        self.maxsize = maxsize

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(maxsize={self.maxsize}, data={self.__data_repr__()})"

    def __getitem__(self, key: str) -> T:
        return self._data[key]

    def __setitem__(self, key: str, value: T) -> None:
        if len(self._data) >= self.maxsize:
            self._data.popitem(last=False)
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def popitem(self) -> tuple[str, T]:
        return self._data.popitem(last=False)


class LFUCache(Cache[T]):
    def __init__(self, maxsize: int = 256) -> None:
        super().__init__()
        self._counter: Counter[str] = Counter()
        self.maxsize = maxsize

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(maxsize={self.maxsize}, data={self.__data_repr__()})"

    def __getitem__(self, key: str) -> T:
        value = self._data[key]
        self._counter[key] += 1
        self._sort_values()
        return value

    def __setitem__(self, key: str, value: T) -> None:
        if key in self._data:
            self._data[key] = value
            self._counter[key] += 1
        else:
            if len(self._data) >= self.maxsize:
                min_item = min(self._counter.items(), key=lambda x: x[1])
                del self._data[min_item[0]]
                del self._counter[min_item[0]]
            self._data[key] = value
            self._counter[key] = 1
        self._sort_values()

    def __delitem__(self, key: str) -> None:
        del self._data[key]
        del self._counter[key]

    def clear(self) -> None:
        self._data.clear()
        self._counter.clear()

    def _sort_values(self):
        self._data = OrderedDict(
            sorted(self._data.items(), key=lambda kv: self._counter[kv[0]], reverse=True),
        )

    def __data_repr__(self) -> dict[str, tuple[T, int]]:
        return {k: (v, self._counter[k]) for k, v in self._data.items()}


class LRUCache(Cache[T]):
    def __init__(self, maxsize: int = 256) -> None:
        super().__init__()
        self.maxsize = maxsize

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(maxsize={self.maxsize}, data={self.__data_repr__()})"

    def __getitem__(self, key: str) -> T:
        value = self._data[key]
        self._data.move_to_end(key)
        return value

    def __setitem__(self, key: str, value: T) -> None:
        self._data[key] = value
        if len(self._data) > self.maxsize:
            self._data.popitem(last=False)


class MRUCache(Cache[T]):
    def __init__(self, maxsize: int = 256) -> None:
        super().__init__()
        self.maxsize = maxsize

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(maxsize={self.maxsize}, data={self.__data_repr__()})"

    def __getitem__(self, key: str) -> T:
        value = self._data[key]
        self._data.move_to_end(key, last=False)
        return value

    def __setitem__(self, key: str, value: T) -> None:
        self._data[key] = value
        if len(self._data) > self.maxsize:
            self._data.popitem(last=False)
        self._data.move_to_end(key, last=False)

    def get(self, key: str, default: T | None = None) -> T | None:
        if key in self._data:
            self._data.move_to_end(key, last=False)
            return self._data[key]
        return default

    def setdefault(self, key: str, default: T) -> T:
        if key in self._data:
            self._data.move_to_end(key, last=False)
            return self._data[key]
        self._data[key] = default
        if len(self._data) > self.maxsize:
            self._data.popitem(last=True)
        return default


class TTLCache(Cache[T]):
    def __init__(self, ttl: timedelta | int = 60) -> None:
        super().__init__()
        self._expire_times: dict[str, int] = {}
        if isinstance(ttl, timedelta):
            self.ttl = int(ttl.total_seconds())
        else:
            self.ttl = ttl

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(ttl={self.ttl}s, data={self.__data_repr__()})"

    def __getitem__(self, key: str) -> T:
        self.expire()
        return self._data[key]

    def __setitem__(self, key: str, value: T) -> None:
        self._data[key] = value
        self._expire_times[key] = int(time.time()) + self.ttl

    def __delitem__(self, key: str) -> None:
        del self._data[key]
        del self._expire_times[key]

    def set(self, key: str, value: T, ttl: timedelta | int | None = None):
        if isinstance(ttl, timedelta):
            ttl = int(ttl.total_seconds())
        elif ttl is None:
            ttl = self.ttl
        self._data[key] = value
        self._expire_times[key] = int(time.time()) + ttl

    def get_and_refresh(self, key: str, default: T | None = None, ttl: timedelta | int | None = None) -> T | None:
        value = self[key]
        if value is None:
            return default
        if isinstance(ttl, timedelta):
            ttl = int(ttl.total_seconds())
        elif ttl is None:
            ttl = self.ttl
        self._expire_times[key] = int(time.time()) + ttl
        return value

    def clear(self) -> None:
        self._data.clear()
        self._expire_times.clear()

    def expire(self):
        now_time = int(time.time())
        self._expire_times = {k: v for k, v in self._expire_times.items() if now_time < v}
        self._data = OrderedDict({k: v for k, v in self._data.items() if k in self._expire_times})

    def __data_repr__(self) -> dict[str, tuple[T, int]]:
        self.expire()
        now_time = int(time.time())
        return {k: (v, self._expire_times[k] - now_time) for k, v in self._data.items()}


class TLRUCache(Cache[T]):
    def __init__(self, maxsize: int = 256, ttl: timedelta | int = 60) -> None:
        super().__init__()
        self.maxsize = maxsize
        self._expire_times: dict[str, int] = {}
        if isinstance(ttl, timedelta):
            self.ttl = int(ttl.total_seconds())
        else:
            self.ttl = ttl

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(maxsize={self.maxsize}, ttl={self.ttl}s, data={self.__data_repr__()})"

    def __getitem__(self, key: str) -> T:
        self.expire()
        value = self._data[key]
        self._data.move_to_end(key)
        return value

    def __setitem__(self, key: str, value: T) -> None:
        self._data[key] = value
        self._expire_times[key] = int(time.time()) + self.ttl
        if len(self._data) > self.maxsize:
            pop_key, _ = self._data.popitem(last=False)
            del self._expire_times[pop_key]

    def __delitem__(self, key: str) -> None:
        del self._data[key]
        del self._expire_times[key]

    def set(self, key: str, value: T, ttl: timedelta | int | None = None):
        if isinstance(ttl, timedelta):
            ttl = int(ttl.total_seconds())
        elif ttl is None:
            ttl = self.ttl
        self._data[key] = value
        self._expire_times[key] = int(time.time()) + ttl
        if len(self._data) > self.maxsize:
            pop_key, _ = self._data.popitem(last=False)
            del self._expire_times[pop_key]

    def get_and_refresh(self, key: str, default: T | None = None, ttl: timedelta | int | None = None) -> T | None:
        try:
            value = self[key]
            self._data.move_to_end(key)
            if isinstance(ttl, timedelta):
                ttl = int(ttl.total_seconds())
            elif ttl is None:
                ttl = self.ttl
            self._expire_times[key] = int(time.time()) + ttl
            return value
        except KeyError:
            return default

    def clear(self) -> None:
        self._data.clear()
        self._expire_times.clear()

    def expire(self):
        now_time = int(time.time())
        self._expire_times = {k: v for k, v in self._expire_times.items() if now_time < v}
        self._data = OrderedDict({k: v for k, v in self._data.items() if k in self._expire_times})

    def __data_repr__(self) -> dict[str, tuple[T, int]]:
        self.expire()
        now_time = int(time.time())
        return {k: (v, self._expire_times[k] - now_time) for k, v in self._data.items()}


def gen_signature(
    args: tuple[Any, ...],
    kwds: dict[str, Any],
    kwd_mark=(object(),),
) -> int:
    key = [*args]
    if kwds:
        key.append(kwd_mark)
        key.extend(iter(kwds.items()))
    return hash(tuple(key))


def _decorator(
    cache: Cache,
    hash_func: Callable[..., tuple] | None = None,
    is_method: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def cache_decorator(func: Callable[P, R]) -> Callable[P, R]:
        nonlocal cache
        cache = cast(Cache[R], cache)
        if iscoroutinefunction(func):
            lock = Lock()

            @wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                if is_method:
                    key = (
                        str(hash(*hash_func(*args[1:], **kwargs)))  # type: ignore
                        if hash_func
                        else str(gen_signature(args[1:], kwargs))
                    )
                else:
                    key = str(hash(*hash_func(*args, **kwargs))) if hash_func else str(gen_signature(args, kwargs))
                async with lock:
                    try:
                        return cache[key]
                    except KeyError:
                        value = await func(*args, **kwargs)
                        cache[key] = value
                        return value

            async_wrapper.no_cache = func  # type: ignore
            return async_wrapper  # type: ignore
        lock = RLock()

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if is_method:
                key = (
                    str(hash(*hash_func(*args[1:], **kwargs)))  # type: ignore
                    if hash_func
                    else str(gen_signature(args[1:], kwargs))
                )
            else:
                key = str(hash(hash_func(*args, **kwargs))) if hash_func else str(gen_signature(args, kwargs))
            with lock:
                try:
                    return cache[key]
                except KeyError:
                    value = func(*args, **kwargs)
                    cache[key] = value
                    return value

        wrapper.no_cache = func  # type: ignore
        return wrapper

    return cache_decorator


def cache(
    hash_func: HashFunc | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    return _decorator(Cache(), hash_func)


def cache_method(hash_func: HashFunc | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    return _decorator(Cache(), hash_func, True)


def fifo_cache(
    maxsize: int = 256,
    hash_func: HashFunc | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    return _decorator(FIFOCache(maxsize=maxsize), hash_func)


def fifo_cache_method(
    maxsize: int = 256,
    hash_func: HashFunc | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    return _decorator(FIFOCache(maxsize=maxsize), hash_func, True)


def lfu_cache(
    maxsize: int = 256,
    hash_func: HashFunc | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    return _decorator(LFUCache(maxsize=maxsize), hash_func)


def lfu_cache_method(
    maxsize: int = 256,
    hash_func: HashFunc | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    return _decorator(LFUCache(maxsize=maxsize), hash_func, True)


def lru_cache(
    maxsize: int = 256,
    hash_func: HashFunc | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    return _decorator(LRUCache(maxsize=maxsize), hash_func)


def lru_cache_method(
    maxsize: int = 256,
    hash_func: HashFunc | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    return _decorator(LRUCache(maxsize=maxsize), hash_func, True)


def mru_cache(
    maxsize: int = 256,
    hash_func: HashFunc | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    return _decorator(MRUCache(maxsize=maxsize), hash_func)


def mru_cache_method(
    maxsize: int = 256,
    hash_func: HashFunc | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    return _decorator(MRUCache(maxsize=maxsize), hash_func, True)


def ttl_cache(
    ttl: timedelta | int = 60,
    hash_func: HashFunc | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    if isinstance(ttl, timedelta):
        ttl = int(ttl.total_seconds())
    return _decorator(TTLCache(ttl=ttl), hash_func)


def ttl_cache_method(
    ttl: timedelta | int = 60,
    hash_func: HashFunc | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    if isinstance(ttl, timedelta):
        ttl = int(ttl.total_seconds())
    return _decorator(TTLCache(ttl=ttl), hash_func, True)


def tlru_cache(
    maxsize: int = 256,
    ttl: timedelta | int = 60,
    hash_func: HashFunc | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    if isinstance(ttl, timedelta):
        ttl = int(ttl.total_seconds())
    return _decorator(TLRUCache(maxsize=maxsize, ttl=ttl), hash_func)


def tlru_cache_method(
    maxsize: int = 256,
    ttl: timedelta | int = 60,
    hash_func: HashFunc | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    if isinstance(ttl, timedelta):
        ttl = int(ttl.total_seconds())
    return _decorator(TLRUCache(maxsize=maxsize, ttl=ttl), hash_func, True)
