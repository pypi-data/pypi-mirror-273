from functools import reduce
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TYPE_CHECKING, TypeVar

T = TypeVar("T")


class classproperty(Generic[T]):
    """类属性装饰器"""

    def __init__(self, func: Callable[[Any], T]) -> None:
        self.func = func

    def __get__(self, instance: Any, owner: Optional[Type[Any]] = None) -> T:
        return self.func(type(instance) if owner is None else owner)


if TYPE_CHECKING:
    hybridmethod = classmethod
    """混合方法装饰器"""

else:

    class hybridmethod:
        def __init__(self, func: Callable[..., Any]):
            self.__func__ = func

        def __get__(self, instance: Any, owner: Type[Any] | None = None) -> Any:
            if instance is None:
                return self.__func__.__get__(owner, owner)
            return self.__func__.__get__(instance, owner)


def create_nested_dict(path: List[str], value: Any) -> Dict[str, Any]:
    """创建嵌套字典"""
    if len(path) == 1:
        return {path[0]: value}
    return {path[0]: create_nested_dict(path[1:], value)}


def merge_dict(a: Dict[str, Any], b: Dict[str, Any]):
    """合并字典"""
    result = {}
    keys = list(a.keys()) + list(b.keys())
    for key in keys:
        if key in result:
            pass
        if key in a and key in b and isinstance(a[key], dict) and isinstance(b[key], dict):
            result[key] = merge_dict(a[key], b[key])
        elif key in a:
            result[key] = b[key] if key in b else a[key]
        else:
            result[key] = b[key]
    return result


def generate_dict(data: Dict[str, Any], separator: str = ".") -> Dict[str, Any]:
    """生成字典"""
    result = {}
    for key, value in data.items():
        keys = key.split(separator)
        current_dict = result
        for i, key_part in enumerate(keys):
            if key_part not in current_dict:
                if i == len(keys) - 1:
                    current_dict[key_part] = value
                else:
                    current_dict[key_part] = {}
            current_dict = current_dict[key_part]
    return result


def nested_getattr(obj: Any, keys: List[str]) -> Any:
    """获取嵌套属性"""
    return reduce(
        lambda d, key: getattr(d, key),
        keys,
        obj,
    )


def nested_getitem(obj: Any, keys: List[str]) -> Any:
    """获取嵌套属性"""
    return reduce(
        lambda d, key: d[key],
        keys,
        obj,
    )
