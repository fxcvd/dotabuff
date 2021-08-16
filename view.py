from dotabuff import DotaBuffPlayer
from dotabuff import DotaBuff

import json
import asyncio


def write_table(name, json_table):
    with open(f"{name}.json", "w") as json_file:
        json.dump(json_table, json_file)

async def main():
    #1st method
    player = DotaBuffPlayer(136360208)
    json_table = await player.get_matches(max_count=1) #get matches from class player

    write_table("1st_method", json_table)


    #2nd method
    d2buff = DotaBuff()
    json_table = await d2buff.get_matches(player=136360208, max_count=1) #get matches from argument player

    write_table("2nd_method", json_table)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())