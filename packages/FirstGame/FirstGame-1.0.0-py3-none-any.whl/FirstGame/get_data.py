import pymysql
import random
import re
import yaml
import os
import sys

"""打包相關"""
# 將所需檔案新增至此Python檔案
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 連結database
def connect_to_database():
    with open(resource_path('database.yml'), 'r') as file:
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
        return conn
    except Exception as ex:
        print(ex)
        return None

# 判定是否註冊過
def ok_user_id(user_id):
    conn = connect_to_database()
    if conn:
        try:
            # 建立Cursor物件
            with conn.cursor() as cursor:
                # 查詢資料SQL語法
                command = "SELECT username, password FROM user WHERE username=%s"
                # 執行指令
                cursor.execute(command,(user_id,))
                # 取得所有資料
                result = cursor.fetchall()
                print(result)
        except Exception as ex:
            print(ex)

        if result:
            # 在result中找到了user_id
            password = result[0][1]
        else:
            # result為空，沒有找到匹配的user_id
            password = ''
        return password

# 取得前10排名
def get_ranking(now, user_id, score, total, level, topic):
    conn = connect_to_database()
    if conn:
        try:
            # 建立Cursor物件
            with conn.cursor() as cursor:
                # 新增資料SQL語法
                command = "INSERT INTO charts(time, name, score, total, level, topic)VALUES(%s, %s, %s, %s, %s, %s)"
                # 新增"結束時間", "使用者名稱", "遊戲分數", "題數", "難易度", "主題"給資料庫
                cursor.execute(command, (now, user_id, score, total, level, topic))
                # 儲存變更
                conn.commit()

                # 查詢資料SQL語法
                command = "SELECT DISTINCT name, score, time FROM charts WHERE level = %s AND total = %s AND topic = %s ORDER BY score DESC LIMIT 10"
                # 執行指令
                cursor.execute(command, (level, total, topic))
                # 取得所有資料
                result = cursor.fetchall()
                
        except Exception as ex:
            print(ex)

        return result

# 註冊帳號資料
def register_user(username, password):
    conn = connect_to_database()
    try:
        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料SQL語法
            command = "INSERT INTO user(username, password)VALUES(%s, %s)"
            cursor.execute(command, (username, password))
            # 儲存變更
            conn.commit()
    except Exception as ex:
        print(ex)

# 取得圖片二進制資料
def get_picture_data(selected_topic, group_name):
    global selected_pictures
    conn = connect_to_database()
    try: 
        # 建立Cursor物件
        with conn.cursor() as cursor:
            if selected_topic == 'anime':
                command = "SELECT picture, name, group_name FROM anime WHERE group_name=%s"
            elif selected_topic == 'kpop':
                command = "SELECT picture, name, group_name FROM kpop WHERE group_name=%s"
            cursor.execute(command, (group_name))
            result = cursor.fetchall()
            selected_pictures += result
        # 儲存
        conn.commit()
    except Exception as ex:
        print(ex)

# 取得選取圖檔的二進制
def get_random_jpg(selected_topic, groups):
    global selected_pictures
    selected_pictures = []
    pictures = []
    answers = []
    group_names = []

    for group_name in groups:
        get_picture_data(selected_topic, group_name)

    random.shuffle(selected_pictures)

    for i in selected_pictures:
        picture = i[0]
        name = i[1]
        group = i[2]
        # 將尾巴數字去掉變成答案
        answer = re.sub(r'\d+', '', name)

        pictures.append(picture)
        answers.append(answer)
        group_names.append(group)
    return answers, pictures, group_names
