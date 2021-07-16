"""Asynchronous Python client for the Forecast.Solar API."""
from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from dataclasses import InitVar, dataclass
from typing import Any

from aiodns import DNSResolver
from aiodns.error import DNSError
from aiohttp import ClientSession, ClientResponse
from yarl import URL

from .exceptions import (
    ForecastSolarConnectionError,
    ForecastSolarError,
    ForecastSolarRequestError,
    ForecastSolarRatelimit,
)
from .models import Estimate


@dataclass
class Ratelimit:
    """Information about the current rate limit."""

    call_limit: int
    remaining_calls: int
    period: int
    retry_at: datetime | None

    @classmethod
    def from_response(cls, response: ClientResponse) -> Ratelimit:
        """Initialize rate limit object from response."""
        from pprint import pprint

        pprint(dict(response.headers))
        # The documented headers do not match the returned headers
        # https://doc.forecast.solar/doku.php?id=api#headers
        limit = int(response.headers["X-Ratelimit-Limit"])
        period = int(response.headers["X-Ratelimit-Period"])

        # Remaining is not there if we exceeded limit
        remaining = int(response.headers.get("X-Ratelimit-Remaining", 0))

        if "X-Ratelimit-Retry-At" in response.headers:
            retry_at = datetime.fromisoformat(response.headers["X-Ratelimit-Retry-At"])
        else:
            retry_at = None

        return cls(limit, period, remaining, retry_at)


@dataclass
class ForecastSolar:
    """Main class for handling connections with the Forecast.Solar API."""

    azimuth: float
    declination: float
    kwp: float
    latitude: float
    longitude: float

    api_key: str | None = None
    close_session: bool = False
    damping: float = 0
    session: ClientSession | None = None
    ratelimit: Ratelimit | None = None

    async def _request(
        self,
        uri: str,
        *,
        params: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        """Handle a request to the Forecast.Solar API.

        A generic method for sending/handling HTTP requests done against
        the Forecast.Solar API.

        Args:
            uri: Request URI, for example, 'estimate'

        Returns:
            A Python dictionary (JSON decoded) with the response from
            the Forecast.Solar API.

        Raises:
            ForecastSolarConnectionError: An error occurred while communicating
                with the Forecast.Solar API.
            ForecastSolarError: Received an unexpected response from the
                Forecast.Solar API.
            ForecastSolarRequestError: There is something wrong with the
                variables used in the request.
            ForecastSolarRatelimit: The number of requests has exceeded
                the rate limit of the Forecast.Solar API.
        """

        # Forecast.Solar is currently experiencing IPv6 issues.
        # However, their DNS does return an non-working IPv6 address.
        # This ensures we use the IPv4 address.
        dns = DNSResolver()
        try:
            result = await dns.query("api.forecast.solar", "A")
        except DNSError as err:
            raise ForecastSolarConnectionError(
                "Error while resolving Forecast.Solar API address"
            ) from err

        if not result:
            raise ForecastSolarConnectionError(
                "Could not resolve Forecast.Solar API address"
            )

        # Connect as normal
        url = URL.build(scheme="https", host=result[0].host)

        # Add API key if one is provided
        if self.api_key is not None:
            url = url.with_path(f"{self.api_key}/")

        url = url.join(URL(uri))

        if self.session is None:
            self.session = ClientSession()
            self.close_session = True

        response = await self.session.request(
            "GET",
            url,
            params=params,
            headers={"Host": "api.forecast.solar"},
            ssl=False,
        )

        if response.status < 500:
            self.ratelimit = Ratelimit.from_response(response)

        if response.status == 400:
            data = await response.json()
            raise ForecastSolarRequestError(data["message"])

        if response.status == 429:
            data = await response.json()
            raise ForecastSolarRatelimit(data["message"])

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise ForecastSolarError(
                "Unexpected response from the Forecast.Solar API",
                {"Content-Type": content_type, "response": text},
            )

        return await response.json()

    async def estimate(self) -> Estimate:
        """Get solar production estimations from the Forecast.Solar API.

        Returns:
            A Estimate object, with a estimated production forecast.

        Raises:
            ForecastSolarRequestError: There is something wrong with the
                variables used in the request.
        """
        data = await self._request(
            f"estimate/{self.latitude}/{self.longitude}"
            f"/{self.declination}/{self.azimuth}/{self.kwp}",
            params={"time": "iso8601", "damping": str(self.damping)},
        )

        if not data["result"]["watts"]:
            raise ForecastSolarRequestError(
                "The location isn't in the data coverage zone of the Forecast.Solar API"
            )

        return Estimate.from_dict(data)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self.close_session:
            await self.session.close()

    async def __aenter__(self) -> ForecastSolar:
        """Async enter.

        Returns:
            The ForecastSolar object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.close()
