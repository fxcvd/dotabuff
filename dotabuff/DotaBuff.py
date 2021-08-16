import aiohttp
import asyncio

from requests import Session
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


base_url = "https://ru.dotabuff.com"


session = Session() #init session

session.headers.update({
    "user-agent": UserAgent().random
}) #session with browser user agent


class DotaBuff(object):
    def __init__(self):
        pass

    async def get_matches(self, player, page=1, max_count=50):
        url = f"https://ru.dotabuff.com/players/{player}/matches?lobby_type=ranked_matchmaking&game_mode=all_pick&page={page}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"user-agent": UserAgent().random}) as resp:
                html = await resp.text() #get matches via http request
        
        soup = BeautifulSoup(html, "html.parser") #decode text to html format
        match_table = soup.find_all("section")[2].find("article").find("table").find("tbody").find_all("tr")

        matches = []
        index = 0
        for table_item in match_table:
            if index >= max_count:
                break

            hero = table_item.find(class_="cell-large").find("a").text
            hero_img = base_url + table_item.find("img", class_="image-hero")["src"]
            match_url = base_url + table_item.find(class_="cell-large").find("a")["href"]
            kda = table_item.find("span", class_="kda-record").text
            time = table_item.find_all("td")[5].text
            

            items = []
            for item in table_item.find("td", class_="r-none-tablet cell-xxlarge").find_all("a"):
                item_url = base_url + item["href"]
                item_image = base_url + item.find("img")["src"]
                item_name = item.find("img").get("title")

                items.append({
                    "url": item_url,
                    "name": item_name,
                    "image": item_image
                })


            matches.append({
                "hero": {
                    "name": hero,
                    "image": hero_img
                },
                "macth": {
                    "id": match_url.split("/")[-1],
                    "url": match_url
                },
                "kda": kda,
                "time": time,
                "items": items
            })


            index += 1

        return matches



