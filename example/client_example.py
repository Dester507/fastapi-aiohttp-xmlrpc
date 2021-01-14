import asyncio
from fastapi_aio.client_edit import ServerProxy


loop = asyncio.get_event_loop()
client = ServerProxy("http://localhost:8080", loop=loop)


async def main():

    # Or via __getitem__
    method = client['sumaa']
    print(await method("TOL", "IK"))

    client.close()


if __name__ == "__main__":
    loop.run_until_complete(main())