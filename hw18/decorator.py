import time
import asyncio
from functools import wraps

def execution_time(func):
    @wraps(func)
    async def wrapper_async(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.6f} seconds (async)")
        return result

    def wrapper_sync(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.6f} seconds (sync)")
        return result

    if asyncio.iscoroutinefunction(func):
        return wrapper_async
    else:
        return wrapper_sync
