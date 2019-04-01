import scrapy
import json


class Bludv(scrapy.Spider):
    name = 'bludv'

    def start_requests(self):
        for x in range(1, 6):
            yield scrapy.Request(url='https://www.bludv.tv/page/' + str(x), callback=self.parse)

    def parse(self, response):
        arr = []
        #f = open('bludv.txt', 'w')

        for post in response.css('div.post'):
            title = post.css('div.title a::text').extract_first()
            link = post.css(
                'div.content a.more-link::attr("href")').extract_first()
            img = post.css(
                'div.content div.separator img::attr("src")').extract_first()

            arr.append({
                'title': title,
                'link': link,
                'image': img
            })
            #str_post = title + ' - Link: '+link+' img: '+img
            # f.write(str_post)

        with open('bludv.txt', 'a+', encoding="utf8") as f:
            json.dump(arr, f)
            # self.log(f)
