from __future__ import annotations
import dataclasses
from cmu_112_graphics.cmu_112_graphics import App
from functools import lru_cache, wraps
from typing import Any, Protocol, final


class MouseEventLike(Protocol):
    x: int
    y: int
class KeyEventLike(Protocol):
    key: str


@dataclasses.dataclass
class MouseEventMinimal:
    x: int
    y: int

@dataclasses.dataclass
class KeyEventMinimal:
    key: str


class MouseListenerLike(Protocol):
    def __call__(self, app: App, event: MouseEventLike) -> Any: ...
class KeyListenerLike(Protocol):
    def __call__(self, app: App, event: KeyEventLike) -> Any: ...
class SingularListenerLike(Protocol):
    def __call__(self, app: App) -> Any: ...


@dataclasses.dataclass
class _ESMouseDispatcher:
    call: MouseListenerLike
    app: App
    event: MouseEventMinimal

    def __call__(self) -> None:
        self.call(self.app, self.event)

@dataclasses.dataclass
class _ESKeyDispatcher:
    call: KeyListenerLike
    app: App
    event: KeyEventMinimal

    def __call__(self) -> None:
        self.call(self.app, self.event)

@dataclasses.dataclass
class _ESSingularDispatcher:
    call: SingularListenerLike
    app: App

    def __call__(self) -> None:
        self.call(self.app)


class _ESDispatcherLike(Protocol):
    def __call__(self) -> None: ...
class _DispatcherStorageLike(Protocol):
    def __call__(self, ed: _ESDispatcherLike, /) -> None: ...


@dataclasses.dataclass
class _ESMouseListener:
    call: MouseListenerLike
    store: _DispatcherStorageLike

    def __call__(self, app: App, event: MouseEventLike) -> None:
        eventmin = MouseEventMinimal(event.x, event.y)
        dispatcher = _ESMouseDispatcher(self.call, app, eventmin)
        self.store(dispatcher)

@dataclasses.dataclass
class _ESKeyListener:
    call: KeyListenerLike
    store: _DispatcherStorageLike

    def __call__(self, app: App, event: KeyEventLike) -> None:
        eventmin = KeyEventMinimal(event.key)
        dispatcher = _ESKeyDispatcher(self.call, app, eventmin)
        self.store(dispatcher)

@dataclasses.dataclass
class _ESSingularListener:
    call: SingularListenerLike
    store: _DispatcherStorageLike

    def __call__(self, app: App) -> None:
        dispatcher = _ESSingularDispatcher(self.call, app)
        self.store(dispatcher)


class _ESReregisterError(Exception):
    def __init__(self, call) -> None:
        super().__init__(f"{call} is repeatedly registered")
        self.call = call


@lru_cache(1)  # is singleton (takes no arguments, so fine)
@final         # cannot be subclassed
class _EventSyncronizer:
    '''
    Wrap event listeners and hook them to a repeatedly-called function, to
    guarantee that event listeners are

    1. not called simultaneously as any other code;
    2. called right before the hook.

    This eliminates race conditions, ensures a definitive execution order, and
    also leverages the listener paradigm for code organization.

    Usage example:

        @ESync.mouse  # XXX added as a decorator
        def mousePressed(app, event):
            ...  # do stuff as normal

        @ESync.key  # similar but for key events
        def keyPressed(app, event):
            ...  # do stuff as normal

        @ESync.singular  # also similar but for one-argument listeners
        def sizeChanged(app):
            ...  # do stuff as normal

        @ESync.hook  # this one for `timerFired` in particular
        def timerFired(app):
            ...  # do stuff as normal

    Notes for .singular:

        A "singular" event listener is one that takes only `app` as argument.
        This decorator should NOT be used on `appStarted` or `appStopped`
        because those functions may run without the main loop being active.

    Note for .hook:

        .hook should NOT be used on `redrawAll` because it will cause MVC
        violations.
    '''

    container: list[_ESDispatcherLike]

    def __init__(self) -> None:
        self.container = []

    def _dispatch(self) -> None:
        container = self.container.copy()  # shallow
        self.container.clear()
        for d in container: d()

    def mouse(self, call: MouseListenerLike) -> _ESMouseListener:
        '''
        Wrap a mouse event listener, to eliminate race conditions while
        leveraging the listener paradigm.
        '''
        return _ESMouseListener(call, self.container.append)

    def key(self, call: KeyListenerLike) -> _ESKeyListener:
        '''
        Wrap a key event listener, to eliminate race conditions while leveraging
        the listener paradigm.
        '''
        return _ESKeyListener(call, self.container.append)

    def singular(self, call: SingularListenerLike) -> _ESSingularListener:
        '''
        Wrap a singular event listener, to eliminate race conditions while
        leveraging the listener paradigm.

        A "singular" event listener is one that takes only `app` as argument.
        This decorator should NOT be used on `appStarted` or `appStopped`
        because those functions may run without the main loop being active.
        '''
        return _ESSingularListener(call, self.container.append)

    def hook(self, call):
        '''
        Hook to a repeatedly called function, in particular `timerFired`; will
        guarantee to collect events in normal times and process them in batch
        right before the body of `timerFired` is run.

        .hook should NOT be used on `redrawAll` because it will cause MVC
        violations.
        '''
        @wraps(call)
        def __inner(*a, **kw):
            self._dispatch()
            call(*a, **kw)
        return __inner


ESync = _EventSyncronizer()  # singleton object
