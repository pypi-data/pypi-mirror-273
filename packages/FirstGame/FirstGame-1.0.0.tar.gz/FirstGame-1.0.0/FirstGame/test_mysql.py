import pymysql
import os
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

def convertToBinaryData(filename):
    # 將圖片轉為二進制
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def delete_data():
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            for n in range(606, 881):
                command = "DELETE FROM anime WHERE id=%s"
                cursor.execute(command, (n))

        # 儲存變更
        conn.commit()
    except Exception as ex:
        print(ex)

def get_jpg_names() -> None:
    global kpops, names
    kpops = []
    names = []
    current_dir = os.getcwd()
    kpop_dir = os.path.join(current_dir, 'kpop')
    kpops = os.listdir(kpop_dir)
    for i, kpop in enumerate(kpops):
        kpop_name_dir = os.path.join(kpop_dir, kpop)
        for file_name in os.listdir(kpop_name_dir):
            if file_name.endswith('.jpg'):
                full_path = os.path.join(kpop_name_dir, file_name)
                names.append(full_path)

                binaryData = convertToBinaryData(full_path)
                dir_name = os.path.basename(os.path.dirname(full_path))
                #print(dir_name)
                #print(file_name)
                #print(binaryData)
                add_data(dir_name, file_name[:-4], binaryData)
    return

def add_data(group_name, name, picture) -> None:
    try:
       # 建立Connection物件
        conn = pymysql.connect(**db_settings)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            command = "INSERT INTO kpop(group_name, name, picture)VALUES(%s, %s, %s)"
            cursor.execute(command, (group_name, name, picture))

        # 儲存
        conn.commit()
    except Exception as ex:
        print(ex)
    
    return

def update_data():
    try:
       # 建立Connection物件
        conn = pymysql.connect(**db_settings)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            command = "SELECT id FROM anime"
            cursor.execute(command)
            result = cursor.fetchall()
            for i in result:
                id = i[0]
                id -= 299
                command = "UPDATE anime SET id=%s"
                cursor.execute(command, (id))

        # 儲存
        conn.commit()
    except Exception as ex:
        print(ex)

    
    #return group_name, name, picture
def main() -> None:
    #delete_data()
    #get_jpg_names()
    #add_data()
    #update_data()
    return


main()
