import configparser


#首先得到配置文件的所有分组，然后根据分组逐一展示所有
#for section in cfg.sections():
#    for items in cfg.items(section):
#        print(items)
class MysqlSetting():
    def __init__(self):
        cfg = configparser.ConfigParser()
        cfg.read('./setting.ini', encoding='UTF-8')
        self.MYSQL_HOST = cfg.get('mysql', 'MYSQL_HOST')
        self.MYSQL_PORT = cfg.getint('mysql', 'MYSQL_PORT')
        self.MYSQL_USER = cfg.get('mysql', 'MYSQL_USER')
        self.MYSQL_PASSWORD = cfg.get('mysql', 'MYSQL_PASSWORD')
        self.MYSQL_DATABASE = cfg.get('mysql', 'MYSQL_DATABASE')
        self.MYSQL_CHARSET = cfg.get('mysql', 'MYSQL_CHARSET')


