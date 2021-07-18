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

## Data

This library returns a lot of different data, based on the API:

### Energy
- Total Estimated Energy Production (per day)
- Estimated Energy Production - This Hour
- Estimated Energy Production - Next Hour

### Power
- Highest Power Peak Time - Today
- Highest Power Peak Time - Tomorrow
- Estimated Power Production - Now
- Estimated Power Production - Next Hour
- Estimated Power Production - In +6 Hours
- Estimated Power Production - In +12 Hours
- Estimated Power Production - In +24 Hours

### API Info
- Timezone
- Rate limit
- Rate remaining

## Contributing

Would you like to contribute to the development of this project? Then read the prepared [contribution guidelines](CONTRIBUTING.md) and go ahead!

Thank you for being involved! :heart_eyes:

## License

MIT License

Copyright (c) 2021 Klaas Schoute

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

<!-- MARKDOWN LINKS & IMAGES -->
[maintenance-shield]: https://img.shields.io/maintenance/yes/2021.svg?style=for-the-badge
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
