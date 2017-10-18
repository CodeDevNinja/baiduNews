from MongoHelp import MongoHelper as SqlHelper

import csv,time

SqlH = SqlHelper()
SqlH.init_db('zhiHu','zhihu_all')
headers = ['user_name','answer_comment_1','answer_comment_2','answer_comment_3','article_comment_1','article_comment_2','article_comment_3','answer','user_home_url','article', 'flowing','followers','collect','answer','article']
con ={"$and":[{'article_comment':{"$exists": True}},
                                             {'answer_comment':{"$exists": True}},
                                              {'flowing': {"$exists": True}},
             # {'export_flag': {"$exists": False}}
                                              ]}
#
print(SqlH.count(con))
time.sleep(100)
print(SqlH.count(con))
#
# rows=SqlH.select_csv()
#
# #print(rows)
# with open('zhihu_add_1.csv','w') as f:
#     f_csv = csv.DictWriter(f, headers)
#     f_csv.writeheader()
#     for row in rows:
#         print(row)
#         SqlH.update({"user_home_url":row["user_home_url"]},{"export_flag":"1"})
#         if isinstance(row['answer_comment'],list):
#             print(row['answer_comment'])
#             i = 1
#             for item in row['answer_comment'][:3]:
#                 st ='answer_comment_'+str(i)
#                 row[st] = item
#                 i=i+1
#         row.pop('answer_comment')
#
#         if isinstance(row['article_comment'], list):
#             print(row['article_comment'])
#             i = 1
#             for item in row['article_comment'][:3]:
#                 st = 'article_comment_' + str(i)
#                 row[st] = item
#                 i = i + 1
#
#         row.pop('article_comment')
#         print(row)
#         f_csv.writerow(row)