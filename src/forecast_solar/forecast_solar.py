"""Asynchronous Python client for the Forecast.Solar API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from aiodns import DNSResolver
from aiodns.error import DNSError
from aiohttp import ClientSession
from yarl import URL

from .exceptions import (
    ForecastSolarAuthenticationError,
    ForecastSolarConfigError,
    ForecastSolarConnectionError,
    ForecastSolarError,
    ForecastSolarRatelimitError,
    ForecastSolarRequestError,
)
from .models import Estimate, Ratelimit


@dataclass
class ForecastSolar:
    """Main class for handling connections with the Forecast.Solar API."""

    azimuth: float
    declination: float
    kwp: float
    latitude: float
    longitude: float

    api_key: str | None = None
    damping: float = 0
    damping_morning: float | None = None
    damping_evening: float | None = None
    horizon: str | None = None

    session: ClientSession | None = None
    ratelimit: Ratelimit | None = None
    inverter: float | None = None
    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        *,
        rate_limit: bool = True,
        authenticate: bool = True,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle a request to the Forecast.Solar API.

        A generic method for sending/handling HTTP requests done against
        the Forecast.Solar API.

        Args:
        ----
            uri: Request URI, for example, 'estimate'
            rate_limit: Parse rate limit from response. Set to False for
                endpoints that are missing rate limiting headers in response.
            authenticate: Prefix request with api_key. Set to False for
                endpoints that do not provide authentication.

        Returns:
        -------
            A Python dictionary (JSON decoded) with the response from
            the Forecast.Solar API.

        Raises:
        ------
            ForecastSolarAuthenticationError: If the API key is invalid.
            ForecastSolarConnectionError: An error occurred while communicating
                with the Forecast.Solar API.
            ForecastSolarError: Received an unexpected response from the
                Forecast.Solar API.
            ForecastSolarRequestError: There is something wrong with the
                variables used in the request.
            ForecastSolarRatelimitError: The number of requests has exceeded
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
        if authenticate and self.api_key is not None:
            url = url.with_path(f"{self.api_key}/")

        url = url.join(URL(uri))

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        response = await self.session.request(
            "GET",
            url,
            params=params,
            headers={"Host": "api.forecast.solar"},
            ssl=False,
        )

        if response.status in (502, 503):
            raise ForecastSolarConnectionError("The Forecast.Solar API is unreachable")

        if response.status == 400:
            data = await response.json()
            raise ForecastSolarRequestError(data["message"])

        if response.status in (401, 403):
            data = await response.json()
            raise ForecastSolarAuthenticationError(data["message"])

        if response.status == 422:
            data = await response.json()
            raise ForecastSolarConfigError(data["message"])

        if response.status == 429:
            data = await response.json()
            raise ForecastSolarRatelimitError(data["message"])

        if rate_limit and response.status < 500:
            self.ratelimit = Ratelimit.from_response(response)

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise ForecastSolarError(
                "Unexpected response from the Forecast.Solar API",
                {"Content-Type": content_type, "response": text},
            )

        return await response.json()

    async def validate_plane(self) -> bool:
        """Validate plane by calling the Forecast.Solar API.

        Returns
        -------
            True, if plane is valid.

        """
        await self._request(
            f"check/{self.latitude}/{self.longitude}"
            f"/{self.declination}/{self.azimuth}/{self.kwp}",
            rate_limit=False,
            authenticate=False,
        )

        return True

    async def validate_api_key(self) -> bool:
        """Validate api key by calling the Forecast.Solar API.

        Returns
        -------
            True, if api key is valid

        """
        await self._request("info", rate_limit=False)

        return True

    async def estimate(self) -> Estimate:
        """Get solar production estimations from the Forecast.Solar API.

        Returns
        -------
            A Estimate object, with a estimated production forecast.

        """
        params = {"time": "iso8601", "damping": str(self.damping)}
        if self.inverter is not None:
            params["inverter"] = str(self.inverter)
        if self.horizon is not None:
            params["horizon"] = str(self.horizon)
        if self.damping_morning is not None and self.damping_evening is not None:
            params["damping_morning"] = self.damping_morning
            params["damping_evening"] = self.damping_evening
        data = await self._request(
            f"estimate/{self.latitude}/{self.longitude}"
            f"/{self.declination}/{self.azimuth}/{self.kwp}",
            params=params,
        )

        return Estimate.from_dict(data)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The ForecastSolar object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.

        """
        await self.close()
