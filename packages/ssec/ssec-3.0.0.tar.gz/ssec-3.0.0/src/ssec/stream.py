"""Module containing the `stream` and `stream_async` functions."""

from __future__ import annotations

import asyncio
import http
import logging
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator
    from typing import Literal

    from .event import Event

import httpx

from .common import (
    SSEConfig,
    create_session,
    extract_lines,
    parse_events,
    validate_sse_response,
)
from .constants import (
    DECODER,
    DEFAULT_BACKOFF_DELAY,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_CONNECT_TIMEOUT,
    DEFAULT_MAX_CONNECT_ATTEMPTS,
    DEFAULT_RECONNECT_TIMEOUT,
    SSE_HEADERS,
)

_logger = logging.getLogger("ssec")


def stream(
    url: str,
    *,
    session: httpx.Client | None = None,
    connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
    method: Literal["GET", "POST"] = "GET",
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    max_connect_attempts: int = DEFAULT_MAX_CONNECT_ATTEMPTS,
    reconnect_timeout: float = DEFAULT_RECONNECT_TIMEOUT,
    backoff_delay: float = DEFAULT_BACKOFF_DELAY,
) -> Iterator[Event]:
    """Stream server-sent events (SSEs), synchronously.

    Parameters
    ----------
    url
        The URL to stream server-sent events from.
    session
        An optional HTTP session to use for the request.
    connect_timeout
        The timeout for connecting to the server, in seconds.
        Only used if `session` is `None`.
    method
        The HTTP method to use for the request.
    chunk_size
        The size of the chunks to read from the response, in bytes.
    max_connect_attempts
        The maximum number of attempts to connect to the server.
    reconnect_timeout
        The time to wait before reconnecting to the server, in seconds.
    backoff_delay
        The additional time to wait to ease a potentially overloaded server, in seconds.
        This time is exponentiated by the number of connectioin attempts.
    """
    if session is None:
        session = create_session(httpx.Client, connect_timeout=connect_timeout)

    config = SSEConfig(reconnect_timeout=reconnect_timeout, last_event_id="")
    with session:
        connect_attempt = 0
        while True:
            headers = SSE_HEADERS.copy()
            if config.last_event_id:
                headers["Last-Event-ID"] = config.last_event_id

            try:
                with session.stream(method, url, headers=headers) as response:
                    validate_sse_response(response)

                    if response.status_code == http.HTTPStatus.NO_CONTENT:
                        _logger.info("Client was told to stop reconnecting.")
                        break

                    config.origin = str(response.url)

                    connect_attempt = 0
                    _logger.info(f"Connected to {url!r}.")

                    buffer = ""
                    for chunk in response.iter_bytes(chunk_size=chunk_size):
                        buffer += DECODER.decode(chunk)
                        lines, buffer = extract_lines(buffer)
                        yield from parse_events(lines, config)

            except httpx.HTTPError:
                if connect_attempt >= max_connect_attempts:
                    _logger.exception(f"Failed to connect to {url!r}!")
                    raise

                waiting_period = config.reconnect_timeout
                if connect_attempt > 0:
                    waiting_period += backoff_delay**connect_attempt

                message = (
                    f"Failed to connect to {url!r}. "
                    f"Reconnect in {waiting_period} seconds "
                    f"[attempt {connect_attempt + 1}/{max_connect_attempts}]."
                )
                _logger.info(message)

                connect_attempt += 1
                time.sleep(waiting_period)


async def stream_async(
    url: str,
    *,
    session: httpx.AsyncClient | None = None,
    connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
    method: Literal["GET", "POST"] = "GET",
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    max_connect_attempts: int = DEFAULT_MAX_CONNECT_ATTEMPTS,
    reconnect_timeout: float = DEFAULT_RECONNECT_TIMEOUT,
    backoff_delay: float = DEFAULT_BACKOFF_DELAY,
) -> AsyncIterator[Event]:
    """Stream server-sent events (SSEs), asynchronously.

    Parameters
    ----------
    url
        The URL to stream server-sent events from.
    session
        An optional HTTP session to use for the request.
    connect_timeout
        The timeout for connecting to the server, in seconds.
        Only used if `session` is `None`.
    method
        The HTTP method to use for the request.
    chunk_size
        The size of the chunks to read from the response, in bytes.
    max_connect_attempts
        The maximum number of attempts to connect to the server.
    reconnect_timeout
        The time to wait before reconnecting to the server, in seconds.
    backoff_delay
        The additional time to wait to ease a potentially overloaded server, in seconds.
        This time is exponentiated by the number of connectioin attempts.
    """
    if session is None:
        session = create_session(httpx.AsyncClient, connect_timeout=connect_timeout)

    config = SSEConfig(reconnect_timeout=reconnect_timeout, last_event_id="")
    async with session:
        connect_attempt = 0
        while True:
            headers = SSE_HEADERS.copy()
            if config.last_event_id:
                headers["Last-Event-ID"] = config.last_event_id

            try:
                async with session.stream(method, url, headers=headers) as response:
                    validate_sse_response(response)

                    if response.status_code == http.HTTPStatus.NO_CONTENT:
                        _logger.info("Client was told to stop reconnecting.")
                        break

                    config.origin = str(response.url)

                    connect_attempt = 0
                    _logger.info(f"Connected to {url!r}.")

                    buffer = ""
                    async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                        buffer += DECODER.decode(chunk)
                        lines, buffer = extract_lines(buffer)
                        for event in parse_events(lines, config):
                            yield event

            except httpx.HTTPError:
                if connect_attempt >= max_connect_attempts:
                    _logger.exception(f"Failed to connect to {url!r}!")
                    raise

                waiting_period = config.reconnect_timeout
                if connect_attempt > 0:
                    waiting_period += backoff_delay**connect_attempt

                message = (
                    f"Failed to connect to {url!r}. "
                    f"Reconnect in {waiting_period} seconds "
                    f"[attempt {connect_attempt + 1}/{max_connect_attempts}]."
                )
                _logger.info(message)

                connect_attempt += 1
                await asyncio.sleep(waiting_period)
