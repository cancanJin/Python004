import scrapy

from job1.items import Job1Item


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        for base_info in scrapy.Selector(response).xpath("//div[@class=\"movie-hover-info\"]"):
            item = Job1Item()
            movie_title = base_info.xpath("./div[1]/@title").extract_first().strip()
            movie_type = base_info.xpath("./div[2]/text()").extract_first().strip()
            movie_time = base_info.xpath("./div[last()]/text()").extract_first().strip()
            item["movie_title"] = movie_title
            item["movie_type"] = movie_type
            item["movie_time"] = movie_time
            yield item

