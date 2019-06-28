import scrapy
import json
import sqlite3
from datetime import date


class Bludv(scrapy.Spider):
    name = 'bludv_2'

    def start_requests(self):
        for x in range(1, 100):
            page = 90 - x
            if (page > 0):
                yield scrapy.Request(url='https://www.bludv.tv/page/' + str(page), callback=self.parse)

    def parse(self, response):
        arr = []
        data_atual = date.today()

        conn = sqlite3.connect("./database.db")
        c = conn.cursor()

        for post in response.css('div.post'):
            title = post.css('div.title a::text').extract_first()
            link = post.css(
                'div.content a.more-link::attr("href")').extract_first()
            img = post.css(
                'div.content div.separator img::attr("src")').extract_first()

            arr.append({
                'title': title,
                'link': link,
                'image': img,
                'date': data_atual
            })

            c.execute("""
            select count(*) as total from link_filmes 
            where nome = ?
            """, (title,))
            result = c.fetchone()[0]

            if(result == 0):
                c.execute("""
                INSERT INTO link_filmes (nome, link, img, data)
                VALUES (?,?,?,?)
                """, (title, link, img, data_atual))
                conn.commit()

        # with open('bludv.json', 'a+', encoding="utf8") as f:
        #    json.dump(arr, f)
        conn.close()
