# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class Job1Pipeline:
    connection_info = {"host": "127.0.0.1",
                       "port": 3306,
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


class Job1MysqlPipeline:

    # 打开数据库
    def open_spider(self, spider):
        self.db_connection = pymysql.connect(host=spider.settings.get("MYSQL_HOST", "127.0.0.1"),
                                             port=spider.settings.get("MYSQL_PORT", 3306),
                                             user=spider.settings.get("MYSQL_USER", "root"),
                                             password=spider.settings.get("MYSQL_PASSWORD", "root@123"),
                                             database=spider.settings.get("MYSQL_DATABASE", "test-mysql"),
                                             charset=spider.settings.get("MYSQL_CHARSET", "utf8mb4"))
        self.db_cursor = self.db_connection.cursor()

    # 关闭数据库
    def close_spider(self, spider):
        self.db_cursor.close()
        self.db_connection.close()

    sql = "insert into movie_maoyan(movie_title,movie_type,movie_time) values (%s,%s,%s)"

    def process_item(self, item, spider):
        connection = self.db_connection
        cursor = self.db_cursor
        try:
            cursor.execute(self.sql, (item["movie_title"], item["movie_type"], item["movie_time"]))
            connection.commit()
        except Exception as e:
            print(e)
            connection.rollback()
        return item
