# Käytetty GitHubista löytyvää pytile-kirjastoa: https://github.com/bachya/pytile

import asyncio

from aiohttp import ClientSession

from pytile import async_login

import csv
from datetime import datetime

# Korvaa omilla Tile-tunnuksilla
EMAIL = "YOUR_EMAIL"
PASSWORD = "YOUR_PASSWORD"

last_seen = {}

async def main() -> None:
    async with ClientSession() as session:
        # Kirjautuminen Tile-tilille
        api = await async_login(EMAIL, PASSWORD, session)

        # csv-tiedoston alustus
        with open('tile_havainnot.csv', 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["timestamp", "lat", "lon", "last_seen"])

        while True:
            # Hakee kaikki Tile-laitteet
            tiles = await api.async_get_tiles()

            for tile_uuid, tile in tiles.items():
                await tile.async_update()

                last = last_seen.get(tile_uuid)
                now = (tile.latitude, tile.longitude, tile.last_timestamp)
                
                # Jos havainto on uusi, tallentaa tiedostoon
                if now != last:
                    last_seen[tile_uuid] = now
                    with open('tile_havainnot.csv', 'a', newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([datetime.now().isoformat(), tile.latitude, tile.longitude, tile.last_timestamp])

                    print(F"Uusi havainto {tile.last_timestamp}")
            
            await asyncio.sleep(60) # Odota 60s 


asyncio.run(main())