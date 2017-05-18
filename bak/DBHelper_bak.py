import os
import sqlite3
from config import *


class DBHelper:
    conn = None

    def __init__(self):
        dir = os.getcwd() + os.path.sep + 'db'
        if not os.path.exists(dir):
            os.makedirs(dir)
        self.conn = sqlite3.connect(dir + os.path.sep + DB_NAME)
        self.__create_tables()

    def __create_tables(self):
        cursor = self.conn.cursor();
        sql_create_types = 'CREATE TABLE IF NOT EXISTS ' + TABLE_TYPES \
                           + ' (' \
                           + COLUMN_ID + ' INTEGER PRIMARY KEY AUTOINCREMENT,' \
                           + COLUMN_TYPE + ' CHAR(20)' \
                           + ' )'
        cursor.execute(sql_create_types)
        sql_create_sub_types = 'CREATE TABLE IF NOT EXISTS ' + TABLE_SUB_TYPES \
                               + ' (' \
                               + COLUMN_ID + ' INTEGER PRIMARY KEY AUTOINCREMENT,' \
                               + COLUMN_TYPE + ' CHAR(20),' \
                               + COLUMN_SUB_TYPE + ' CHAR(20)' \
                               + ' )'
        cursor.execute(sql_create_sub_types)

        sql_create_books = 'CREATE TABLE IF NOT EXISTS ' + TABLE_BOOKS \
                           + ' (' \
                           + COLUMN_ID + ' INTEGER PRIMARY KEY AUTOINCREMENT,' \
                           + COLUMN_TYPE + ' CHAR(20),' \
                           + COLUMN_SUB_TYPE + ' CHAR(20),' \
                           + COLUMN_TITLE + ' CHAR(50),' \
                           + COLUMN_COVER + ' CHAR(256),' \
                           + COLUMN_AUTHOR + ' CHAR(50),' \
                           + COLUMN_SCORE + ' FLOAT,' \
                           + COLUMN_SCORE_COUNT + ' INTEGER,' \
                           + COLUMN_FAVORITE + ' INTEGER,' \
                           + COLUMN_DETAIL_LINK + ' CHAR(256),' \
                           + COLUMN_INTRODUCE + ' TEXT' \
                           + ' )'
        cursor.execute(sql_create_books)
        cursor.close()

    def insert_types(self, type):
        print('inserting types table....', type)
        cursor = self.conn.cursor();
        sql = 'INSERT INTO ' + TABLE_TYPES + ' (' + COLUMN_TYPE + ') VALUES (\"' + type + '\")'
        print(sql)
        cursor.execute(sql)
        self.conn.commit()
        cursor.close()

    def insert_sub_types(self, type, sub_types):
        print('inserting sub_types table....')
        cursor = self.conn.cursor();
        for item in sub_types:
            cursor.execute('INSERT INTO ' + TABLE_SUB_TYPES
                           + ' (' + COLUMN_TYPE + ',' + COLUMN_SUB_TYPE + ') VALUES (\"' + type + '\",\"' + item + '\")')
        self.conn.commit()
        cursor.close()

    def insert_books(self, type, sub_type, books):
        print('inserting books table....')
        cursor = self.conn.cursor();
        sql = 'INSERT INTO ' + TABLE_BOOKS \
              + ' (' + COLUMN_TYPE + ',' + COLUMN_SUB_TYPE + ',' + COLUMN_TITLE + ',' + COLUMN_COVER + ',' + COLUMN_AUTHOR + ',' + COLUMN_SCORE + ',' \
              + COLUMN_SCORE_COUNT + ',' + COLUMN_DETAIL_LINK + ') VALUES (\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\",{5},{6},\"{7}\")'
        # print(sql)
        for item in books:
            # print(item)
            s = sql.format(type, sub_type, item['title'], item['cover_image'], item['author'], item['score'],
                           item['score_count'],item['detail_url'])
            print(s)
            cursor.execute(s)
            self.conn.commit()
        cursor.close()

    def release(self):
        self.conn.close()
