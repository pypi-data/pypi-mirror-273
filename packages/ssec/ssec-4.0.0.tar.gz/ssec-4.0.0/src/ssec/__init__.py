"""Yet another library for server-sent events."""

from .common import SSEConfig
from .event import Event
from .stream import sse, sse_async, stream, stream_async
