import scrapy

from job2.items import Job2Item


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']

    DOMAIN = "https://maoyan.com"
    URL = DOMAIN + "/films?showType=3"

    def start_requests(self):
        yield scrapy.FormRequest(self.URL, callback=self.parse)

    def parse(self, response):
        selector = scrapy.Selector(response)
        all_movie_div = selector.xpath("//div[@class=\"channel-detail movie-item-title\"]")
        i = 0
        for base_info in all_movie_div:
            if i < 10:
                i = i+1
                item = Job2Item()
                movie_detail_href = self.DOMAIN + base_info.xpath("./a/@href").extract_first()
                movie_title = base_info.xpath("./a/text()").extract_first()
                item["movie_title"] = movie_title
                yield scrapy.FormRequest(movie_detail_href, meta={"item": item}, callback=self.parse2)

    def parse2(self, response):
        item = response.meta["item"]
        selector = scrapy.Selector(response)
        ul_info = selector.xpath("//div[@class=\"movie-brief-container\"]/ul")
        movie_types = []
        for type_info in ul_info.xpath(".//a[@class=\"text-link\"]/text()"):
            movie_types.append(type_info.extract())
        item["movie_types"] = movie_types
        movie_date = ul_info.xpath("./li[last()]/text()").extract_first()
        item["movie_date"] = movie_date
        yield item
