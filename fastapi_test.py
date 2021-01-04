from fastapi import FastAPI


app = FastAPI(title="fastapi-aiohttp-xmlrpc")


@app.get('/hello')
def hello_world():
    return {'msg': 'Hello World!!!'}
