
from sanic import Sanic
from sanic.response import json
from MongoHelp import MongoHelper as SqlHelper

class apiNews:
    def __init__(self):
        self.sqlhelper = SqlHelper()

    def queryNews(self,category,pz,page,db_name):
        self.sqlhelper.init_db(db_name)
        newsJson = self.sqlhelper.select(pz,{'category':category},page)
        self.sqlhelper.close_client()
        return newsJson
apiNews=apiNews()
app = Sanic(__name__)
@app.route("/news",methods=['GET'])
async def get_handler(request):
    parameter = request.args
    items=apiNews.queryNews(parameter['category'][0],parameter['pageSize'][0],parameter['page'][0],'baiduNews')
    #print(items[0])
    #return json(items[0])
    #return json({'fromTO': 'BD', 'time': '2017/08/16 22:48:41', 'url': 'http://china.huanqiu.com/article/2017-08/11133572.html?from=bdwz', 'title': '河南一疾控科长被开除党籍 曾兜售"抗艾神药"', 'img_path': '', 'category':'bjectId(59945b4ae807f11050b06bed)', 'secCategory': '', 'content': ''})
    #return json(apiNews.queryNews(parameter['category'][0],parameter['pageSize'][0],parameter['page'][0],'baiduNews'))
    return json({"news" : apiNews.queryNews(parameter['category'][0],parameter['pageSize'][0],parameter['page'][0],'baiduNews')})
@app.route("/wx",methods=['GET'])
async def get_handler(request):
    parameter = request.args
    return json(apiNews.queryNews(parameter['category'][0],parameter['pageSize'][0],parameter['page'][0],'weixin'))

app.run(host="0.0.0.0", port=80, debug=True)
