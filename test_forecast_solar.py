
import aiohttp
import asyncio

import forecast_solar

async def main():
    """ Simple function to test the output. """
    async with aiohttp.ClientSession() as client:

        lat = 52.568690
        lon = 4.570470
        dec = 20
        az = 10
        kwp = 2.400

        result = await forecast_solar.get_request(lat, lon, dec, az, kwp, client)
        print(result)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())