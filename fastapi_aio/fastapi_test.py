from fastapi import FastAPI


app = FastAPI(title="fastapi_aiohttp_xmlrpc")


@app.get('/hello')
def hello_world():
    return {'msg': 'Hello World!!!'}
