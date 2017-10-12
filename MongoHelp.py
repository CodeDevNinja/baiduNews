import time

import pymongo
from ISQLHelp import ISQLHelper

from config import DB_CONFIG


class MongoHelper(ISQLHelper):
    def __init__(self,):
        self.client = pymongo.MongoClient(DB_CONFIG['DB_CONNECT_STRING'], connect=False)

    def init_db(self,db_name,col_name):
        create_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.db = self.client[db_name]
        #self.collection = self.db[create_time]
        #self.collection = self.db['zhihu_1']
        self.collection = self.db[col_name]

    def drop_db(self):
        self.client.drop_database(self.db)

    def insertZhiHu(self, value=None):
        if value:
            self.collection.insert(value)

    def insert(self, value=None):
        if value:
            newsObj = dict(title=value['title'], content=value['content'], category=value['category'],secCategory=value['secCategory'],
                         img_path=value['image'],
                         time =value['time'], fromTO=value['from'],url=value['url'])
            self.collection.insert(newsObj)

    def delete(self, conditions=None):
        if conditions:
            self.collection.remove(conditions)
            return ('deleteNum', 'ok')
        else:
            return ('deleteNum', 'None')

    def update(self, conditions=None, value=None):
        # update({"UserName":"libing"},{"$set":{"Email":"libing@126.com","Password":"123"}})
        if conditions and value:
            self.collection.update(conditions, {"$set": value})
            return {'updateNum': 'ok'}
        else:
            return {'updateNum': 'fail'}
    def select_csv(self, count=None, conditions=None,page=None):

       # items = self.collection.find({}, {'_id': 0})
        #items = self.collection.find(conditions,{'_id':0}, limit=count).skip(int(page)).sort(
        items = self.collection.find({"$and":[{'article_comment':{"$exists": True}},
                                             {'answer_comment':{"$exists": True}},
                                              {'flowing': {"$exists": True}}
                                              ]},{'_id':0,'special_comment':0,"special_url":0,"comment_sort":0,
                                                  "special_follower":0,"special_name":0,"home_page":0})
        results = []
        for item in items:
        #     result = (item['title'], item['url'], item['category'],item['content'],item['img_path'],)
             results.append(item)

        return results
        return items

    def select_home_url(self,condition=None,page=None,count=0):
        items = self.collection.find(condition, {'_id': 0,}, limit=count).skip(page)
        return items

    def select(self, count=None, conditions=None,page=None):
        if count:
            count = int(count)
        else:
            count = 0
        if conditions:
            conditions = dict(conditions)
            conditions_name = ['types', 'protocol']
            for condition_name in conditions_name:
                value = conditions.get(condition_name, None)
                if value:
                    conditions[condition_name] = int(value)
        else:
            conditions = {}
        #items = self.collection.find(conditions,{'_id':0}, limit=count).skip(int(page)).sort(
        items = self.collection.find(conditions,{'_id':0}, limit=count).skip(int(page)).sort(

                [("time", pymongo.DESCENDING)])
        results = []
        for item in items:
        #     result = (item['title'], item['url'], item['category'],item['content'],item['img_path'],)
             results.append(item)

        return results
        print(items)
        return items
    def close_client(self):
        self.client.close()

    def count(self,condition=None):
        condition=dict(condition)
        return self.collection.find(condition).count()


if __name__ == '__main__':
    from MongoHelp import MongoHelper as SqlHelper
    sqlhelper = SqlHelper()
    sqlhelper.init_db('zhihu','zhihu_all')
    pre=sqlhelper.count({})
    print('sum:', str(sqlhelper.count({})))
    time.sleep(10)
    now=sqlhelper.count({})
    # url = sqlhelper.select_home_url({"$and":[{"special_url":{"$exists":True}},{"special_url":{"$ne":"none"}}]},count=100,page=1)
    # print("content",url)
    # for item in url:
    #     print(item)


    #####
    # url = sqlhelper.select_home_url({"special_name":{"$exists":True}},count=100,page=1)
    # for item in url:
    #     print(item)
    #


    # #
    url = sqlhelper.select_home_url({"user_name":"Jack"}, count=100, page=1)
    for item in url:
        print(item)


    print('sum:', pre,now)
    print("precent:",str((now-pre)/10))
    #print  (sqlhelper.select(100,{'category':'guonei'},1))
    #items= sqlhelper.proxys.find({'types':0})
    # for item in items:
    # print item
    # # # print sqlhelper.select(None,{'types':u'0'})
    pass

