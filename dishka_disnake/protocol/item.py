from typing import Protocol, TypeVar, Any, Coroutine

T = TypeVar("T", contravariant=True)

class CallbackProtocol(Protocol[T]):
    def __call__(self, interaction: T, *args: Any, **kwargs: Any) -> Coroutine[..., ..., None]: ...
