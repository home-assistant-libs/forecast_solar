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

## Contributing

Would you like to contribute to the development of this project? Then read the prepared [contribution guidelines](CONTRIBUTING.md) and go ahead!

Thank you for being involved! :heart_eyes:

## Setting up development environment

This Python project is fully managed using the [Poetry][poetry] dependencies
manager.

You need at least:

- Python 3.9+
- [Poetry][poetry-install]

Install all packages, including all development requirements:

```bash
poetry install
```

Poetry creates by default an virtual environment where it installs all
necessary pip packages, to enter or exit the venv run the following commands:

```bash
poetry shell
exit
```

Setup the pre-commit check, you must run this inside the virtual environment:

```bash
pre-commit install
```

*Now you're all set to get started!*

As this repository uses the [pre-commit][pre-commit] framework, all changes
are linted and tested with each commit. You can run all checks and tests
manually, using the following command:

```bash
poetry run pre-commit run --all-files
```

To run just the Python tests:

```bash
poetry run pytest
```

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
