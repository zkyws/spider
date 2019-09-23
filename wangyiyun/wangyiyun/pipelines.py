# -*- coding: utf-8 -*-
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WangyiyunPipeline(object):
    def __init__(self):
        # charset 更改，因为评论会有emoji表情，同时需要更改数据的格式
        self.conn = pymysql.connect(host="localhost",user="root",password="z13530227",database="WangYiYun",port=3306,charset='utf8mb4')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        UserName = item["UserName"]
        Comment_content = item["Comment_content"]
        LikedCount = item["LikedCount"]
        Song_name = item["Song_name"]
        sql = "insert into comment(id,SongName,UserName,CommentContent,LikedCount) value(null,%s,%s,%s,%s)"
        self.cur.execute(sql,(Song_name,UserName,Comment_content,LikedCount))
        self.conn.commit()
        return item

    def close_spider(self,spider):
        self.conn.close()



class Wangyiyun_dbPoolPipeline(object):

    def __init__(self):
        dbparam = {
            'host': '127.0.0.1',
            "port": 3306,
            'user': 'root',
            'password': 'z13530227',
            'database': 'WangYiYun',
            'charset': 'utf8mb4',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool("pymysql",**dbparam)

    def process_item(self,item,spider):
        self.dbpool.runInteraction(self.insert, item)


    def close_spider(self,spider):
        pass

    def insert(self, cursor, item):
        UserName = item["UserName"]
        Comment_content = item["Comment_content"]
        LikedCount = item["LikedCount"]
        Song_name = item["Song_name"]
        sql = "insert into comment(id,SongName,UserName,CommentContent,LikedCount) value(null,%s,%s,%s,%s)"
        cursor.execute(sql,(Song_name,UserName,Comment_content,LikedCount))