from fastapi import FastAPI
from .handler_edit import XMLRPCView


app = FastAPI(title="fastapi_aiohttp_xmlrpc")


class Foo(XMLRPCView):

    @app.get('/hello')
    def hello_world(self):
        return {'msg': 'Hello World!!!'}

    def rpc_hello_world(self):
        return {"msg": "Hello Wolrd"}
