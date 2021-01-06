import asyncio
from fastapi_aio.client_edit import ServerProxy


loop = asyncio.get_event_loop()
client = ServerProxy("http://localhost:8000", loop=loop)


async def main():
    print(await client.test())

    # Or via __getitem__
    method = client['hello_world']
    print(await method())

    client.close()


if __name__ == "__main__":
    loop.run_until_complete(main())