from selenium import webdriver
import time
import threading
import pymysql

from Week03.job2.config import MysqlSetting

area_urls = {'北京': 'https://www.lagou.com/beijing-zhaopin/Python/?labelWords=label',
             '上海': 'https://www.lagou.com/shanghai-zhaopin/Python/?labelWords=label',
             '广州': 'https://www.lagou.com/guangzhou-zhaopin/Python/?labelWords=label',
             '深圳': 'https://www.lagou.com/shenzhen-zhaopin/Python/?labelWords=label'}


def start(area_url, area_job, area=""):
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(area_url)
    # 自动点击给也不要
    browser.find_element_by_class_name("body-btn").click()
    while get_now_page_info(browser, area_job, area):
        get_next_page(browser)
    browser.close()
    save(area_job, area)


# 返回是否需要继续下一页的数据
def get_now_page_info(browser, area_job, area):
    time.sleep(2)
    position_divs = browser.find_elements_by_class_name("position")
    for position in position_divs:
        job_pre_name = position.find_element_by_class_name("p_top").find_element_by_tag_name("h3").text
        job_suf_name = position.find_element_by_class_name("p_top").find_element_by_tag_name("em").text
        job_name = job_pre_name + job_suf_name
        job_salary = position.find_element_by_class_name("p_bot").find_element_by_class_name("money").text
        area_job.append((area, job_name, job_salary))
        if len(area_job) >= 2:
            return False
        else:
            return True


def get_next_page(browser):
    next_page = browser.find_elements_by_class_name("page_no")[-1]
    # 有遮罩  需要代码执行点击操作
    # next_page.click()
    browser.execute_script("$(arguments[0]).click()", next_page)


def save(area_job, area):
    sql = "insert into job(area,job_name,job_salary) values(%s,%s,%s)"
    mysql = MysqlCRUD(sql, area_job)
    mysql.process()
    mysql.close()


class MysqlCRUD():
    def __init__(self, sql, area_job):
        mysql = MysqlSetting()
        self.db_connection = pymysql.connect(host=getattr(mysql, "MYSQL_HOST", "127.0.0.1"),
                                             port=getattr(mysql, "MYSQL_PORT", 3306),
                                             user=getattr(mysql, "MYSQL_USER", "root"),
                                             password=getattr(mysql, "MYSQL_PASSWORD", "root@123"),
                                             database=getattr(mysql, "MYSQL_DATABASE", "test-mysql"),
                                             charset=getattr(mysql, "MYSQL_CHARSET", "utf8mb4"))
        self.db_cursor = self.db_connection.cursor()
        self.sql = sql
        self.area_job = area_job

    def close(self):
        self.db_cursor.close()
        self.db_connection.close()

    def process(self):
        connection = self.db_connection
        cursor = self.db_cursor
        area_job = self.area_job
        sql = self.sql
        try:
            cursor.executemany(sql, area_job)
            connection.commit()
        except Exception as e:
            print(e)
            connection.rollback()


if __name__ == "__main__":
    print("start ...")
    thread_list = []
    for key in area_urls.keys():
        thread = threading.Thread(target=start, args=(area_urls[key], [], key))
        thread.start()
        thread_list.append(thread)
    for i in thread_list:
        i.join()
    print("end ...")
