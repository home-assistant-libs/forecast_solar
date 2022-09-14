<!--
*** To avoid retyping too much info. Do a search and replace for the following:
*** github_username, repo_name
-->

## Python API fetching Solarpanels forecast information.
<!-- PROJECT SHIELDS -->
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE)

[![GitHub Activity][commits-shield]][commits]
[![GitHub Last Commit][last-commit-shield]][commits]
[![Contributors][contributors-shield]][contributors-url]

[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

## About

With this python library you can request data from [forecast.solar](https://forecast.solar) and see what your solar panels may produce in the coming days.

## Installation

```bash
pip install forecast-solar
```

## Data

This library returns a lot of different data, based on the API:

### Energy

- Total Estimated Energy Production - today/tomorrow (kWh)
- Estimated Energy Production - This Hour (kWh)
- Estimated Energy Production - Next Hour (kWh)

### Power

- Highest Power Peak Time - Today (datetime)
- Highest Power Peak Time - Tomorrow (datetime)
- Estimated Power Production - Now (W)
- Estimated Power Production - Next Hour (W)
- Estimated Power Production - In +6 Hours (W)
- Estimated Power Production - In +12 Hours (W)
- Estimated Power Production - In +24 Hours (W)

### API Info

- Timezone
- Rate limit
- Account type
- Rate remaining

## Example

```python
import asyncio

from forecast_solar import ForecastSolar


async def main() -> None:
    """Show example on how to use the library."""
    async with ForecastSolar(
        api_key="YOUR_API_KEY",
        latitude=52.16,
        longitude=4.47,
        declination=20,
        azimuth=10,
        kwp=2.160,
        damping=0,
        damping_morning=0.5,
        damping_evening=0.5,
        horizon="0,0,0,10,10,20,20,30,30",
    ) as forecast:
        estimate = await forecast.estimate()
        print(estimate)


if __name__ == "__main__":
    asyncio.run(main())
```

| Parameter | value type | Description |
| --------- | ---------- | ----------- |
| `api_key` | `str` | Your API key from [forecast.solar](https://forecast.solar) (optional) |
| `declination` | `int` | The tilt of the solar panels (required) |
| `azimuth` | `int` | The direction the solar panels are facing (required) |
| `kwp` | `float` | The size of the solar panels in kWp (required) |
| `damping` | `float` | The damping of the solar panels, [read this][forecast-damping] for more information (optional) |
| `damping_morning` | `float` | The damping of the solar panels in the morning (optional) |
| `damping_evening` | `float` | The damping of the solar panels in the evening (optional) |
| `inverter` | `float` | The maximum power of your inverter in kilo watts (optional) |
| `horizon` | `str` | A list of **comma separated** degrees values, [read this][forecast-horizon] for more information (optional) |

## Contributing

Would you like to contribute to the development of this project? Then read the prepared [contribution guidelines](CONTRIBUTING.md) and go ahead!

Thank you for being involved! :heart_eyes:

## License

MIT License

Copyright (c) 2021-2022 Klaas Schoute

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

<!-- LINKS -->
[forecast-horizon]: https://doc.forecast.solar/doku.php?id=api#horizon
[forecast-damping]: https://doc.forecast.solar/doku.php?id=damping

<!-- MARKDOWN LINKS & IMAGES -->
[maintenance-shield]: https://img.shields.io/maintenance/yes/2022.svg?style=for-the-badge
[contributors-shield]: https://img.shields.io/github/contributors/home-assistant-libs/forecast_solar.svg?style=for-the-badge
[contributors-url]: https://github.com/home-assistant-libs/forecast_solar/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/home-assistant-libs/forecast_solar.svg?style=for-the-badge
[forks-url]: https://github.com/home-assistant-libs/forecast_solar/network/members
[stars-shield]: https://img.shields.io/github/stars/home-assistant-libs/forecast_solar.svg?style=for-the-badge
[stars-url]: https://github.com/home-assistant-libs/forecast_solar/stargazers
[issues-shield]: https://img.shields.io/github/issues/home-assistant-libs/forecast_solar.svg?style=for-the-badge
[issues-url]: https://github.com/home-assistant-libs/forecast_solar/issues
[license-shield]: https://img.shields.io/github/license/home-assistant-libs/forecast_solar.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/home-assistant-libs/forecast_solar.svg?style=for-the-badge
[commits]: https://github.com/home-assistant-libs/forecast_solar/commits/master
[last-commit-shield]: https://img.shields.io/github/last-commit/home-assistant-libs/forecast_solar.svg?style=for-the-badge
