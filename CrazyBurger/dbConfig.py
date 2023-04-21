import pymysql

def get_connection():
    return pymysql.connect(
        host= ('127.0.0.1'),
        database = ('crazy_burger'),
        port= 3308,
        user = ('root'),
        password = ('root')
    )