import asyncio

import aioredis


async def main():
    redis = aioredis.from_url("redis://localhost", decode_responses=True)

    # await redis.hset("user:oleg", mapping={"key1": "value1", "key2": "value2", "key3": 123})
    
    # await redis.expire("user:oleg", time=10)

    # result = await redis.hgetall("user:oleg")
    # print('res', result)

    await redis.hgetall("pending_user:user@example.com")

    await redis.close()


if __name__ == "__main__":
    asyncio.run(main())