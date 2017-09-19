from MongoHelp import MongoHelper as SqlHelper

import csv

SqlH = SqlHelper()
SqlH.init_db('zhihu','zhihu_1')
headers = ['user_name', 'followers', 'collect','home_page','answer','article']
rows=SqlH.select_csv()
#SqlH.insertZhiHu(rows)

print(rows)
with open('zhihu_1.csv','w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(rows)