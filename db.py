# How to work with mysql and Python on windows 10
# https://codesport.io/python-tutorials/python-part-7-integrating-mysql-with-python-on-windows-10/

import pymysql.cursors
import pymysql.err
 
class Db:
    connection = None

    def __init__(self,host,user,password,db):
        try:
            self.connection = pymysql.connect(host=host,
                                    user=user,
                                    password=password,
                                    db=db,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        except pymysql.err.InternalError as e:
            print(e)


    def connect(self):
        return self.connection


    def disconnect(self):
        self.connection.close()
