# -*- coding:utf-8 -*-

##
##from flask import Flask
##from flask.ext import restful
##
##
##app = Flask(__name__)
##api = restful.Api(app) #此处为生成一个api实例
##
##
###类来处理请求内容
##class HelloWorld(restful.Resource):
##    def get(self): #实现get方法
##        return {"hello":"world"} #以资源的方式返回
##
##api.add_resource(HelloWorld,'/') #添加路由
##
##
###本文件测试代码
##if __name__ == '__main__':
##    debug = True
##    app.run(host='127.0.0.1', port=5000)



from flask import Flask
from flask.ext.restful import reqparse, Api, Resource, fields, marshal_with
from flask.ext import restful


app = Flask(__name__)
api = Api(app)

#虚拟数据

TODOS = {
    "todo1":{"task":1},
    "todo2":{"task":2},
    "todo3":{"task":3}
    }

#实例化参数解析器
parser = reqparse.RequestParser()
parser.add_argument("task", type=int, help="亲，咱字输入错了")
#parser.add_argument('task', type=int, help='Please set a int task content!')


class TodoList(Resource):
    def get(self):
        return TODOS, 200, {"Etag": "123"}

    def post(self):
        try:
            args = parser.parse_args()
        except Exception:
            print(Exception)


        todo_id = int(max(TODOS.keys()).lstrip("todo"))+1
        todo_id = "todo%i" % todo_id
        TODOS[todo_id] = {"task": args["task"]}
        return TODOS[todo_id], 201

#定义路由
api.add_resource(TodoList, "/todos", "/all_tasks")

class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task

        self.status = "action"



#本文件测试代码
if __name__ == '__main__':
   debug = True
   app.run(host='127.0.0.1', port=5000)
