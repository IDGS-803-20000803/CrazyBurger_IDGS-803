import pymysql

def get_connection():
    return pymysql.connect(
        host= ('127.0.0.1'),
        database = ('crazy_burger'),
        user = ('crazy'),
        password = ('1234')
    )