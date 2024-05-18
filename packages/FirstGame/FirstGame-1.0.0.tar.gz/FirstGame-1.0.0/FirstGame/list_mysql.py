import pymysql
import yaml

with open('config/database.yml', 'r') as file:
    config = yaml.safe_load(file)

db_settings = {
    "host": config['database']['host'],
    "port": config['database']['port'],
    "user": config['database']['user'],
    "password": config['database']['password'],
    "db": config['database']['db'],
    "charset": config['database']['charset']
}

try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        
        # 查詢資料SQL語法
        #command = "INSERT INTO pic(id, picture)VALUES(%s, %s)"
        #command = "SELECT name FROM kpop WHERE name=%s"
        command = "DELETE FROM user WHERE username = %s"
        cursor.execute(command, ('我沒料'))

        result = cursor.fetchall()
        print(result)
        conn.commit()


except Exception as ex:
    print(ex)
