# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class Job1Pipeline:
    connection_info = {"host": "49.233.168.128",
                       "port": 23306,
                       "user": "root",
                       "password": "root@123",
                       "database": "test-mysql",
                       "charset": "utf8mb4"}

    sql = "insert into movie_maoyan(movie_title,movie_type,movie_time) values (%s,%s,%s)"

    def process_item(self, item, spider):
        connection = pymysql.connect(host=self.connection_info["host"],
                                     port=self.connection_info["port"],
                                     user=self.connection_info["user"],
                                     password=self.connection_info["password"],
                                     database=self.connection_info["database"],
                                     charset=self.connection_info["charset"])
        cursor = connection.cursor()
        try:
            cursor.execute(self.sql, (item["movie_title"], item["movie_type"], item["movie_time"]))
            connection.commit()
        except Exception as e:
            print(e)
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
        return item
