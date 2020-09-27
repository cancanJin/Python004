# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Job2Pipeline:
    def process_item(self, item, spider):
        movie_title = item["movie_title"]
        movie_types = item["movie_types"]
        movie_date = item["movie_date"]
        content = f"movie_title:{movie_title} | movie_types:{movie_types} | movie_date:{movie_date} \r\n"
        with open("./movies.csv", mode="a+", encoding="utf-8") as file:
            file.write(content)
        return item
