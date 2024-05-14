"""Event handlers for the crawler.

This module defines the event handlers that can be used to
do some action when a specific event occurs, like storing information
about the pages crawled, logging errors, or stopping the execution.
The handlers are called with the current `Crawler` instance
(passed through the `crawler` kwarg) and the event data.
"""

from enum import Enum
from typing import TYPE_CHECKING, Protocol, Union

import httpx
from typing_extensions import Self  # type: ignore[attr-defined]

from astel import errors, parsers

if TYPE_CHECKING:
    from astel.crawler import Crawler


class Event(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"
    DONE = "done"
    URL_FOUND = "url_found"


class RequestHandler(Protocol):
    """Handler for requests made by a crawler."""

    def __call__(self, request: httpx.Request, crawler: "Crawler") -> None: ...


class ResponseHandler(Protocol):
    """Handler for responses received by a crawler."""

    def __call__(self, response: httpx.Response, crawler: "Crawler") -> None: ...


class ErrorHandler(Protocol):
    """Handler for errors occurred during a crawler execution."""

    def __call__(
        self, error: errors.Error, crawler: "Crawler", *, reraise: bool = False
    ) -> None: ...


class DoneHandler(Protocol):
    """Handler for when a crawler finishes processing a URL."""

    def __call__(self, url: parsers.Url, crawler: "Crawler") -> None: ...


class UrlFoundHandler(Protocol):
    """Handler for when a URL is found in a page."""

    def __call__(self, url: parsers.Url, crawler: "Crawler") -> None: ...


Handler = Union[
    ResponseHandler, RequestHandler, ErrorHandler, DoneHandler, UrlFoundHandler
]


class EventEmitter(Protocol):
    """Protocol for an event emitter."""

    def emit(
        self,
        event: Event,
        *data: Union[httpx.Request, httpx.Response, errors.Error, parsers.Url],
        crawler: "Crawler",
    ) -> Self: ...

    def on(self, event: Event, handler: Handler) -> Self: ...
