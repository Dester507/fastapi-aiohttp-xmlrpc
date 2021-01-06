from fastapi import FastAPI, Request
from msgpack_asgi import MessagePackMiddleware
# from .handler_edit import XMLRPCView


app = FastAPI(title="fastapi")


@app.get('/')
def foo():
    return {'msg': 'hello world'}


@app.post('/name')
async def goo(request: Request):
    body = await request.json()
    return {'Your name': body['name']}

app = MessagePackMiddleware(app)




