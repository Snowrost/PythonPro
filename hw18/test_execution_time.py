import time
import asyncio
import pytest
from decorator import execution_time

@execution_time
def sync_function():
    time.sleep(1)

@execution_time
async def async_function():
    await asyncio.sleep(1)

# Define pytest tests

def test_sync_function(capsys):
    sync_function()
    captured = capsys.readouterr()
    assert "Function 'sync_function' executed in" in captured.out

@pytest.mark.asyncio
async def test_async_function(capsys):
    await async_function()
    captured = capsys.readouterr()
    assert "Function 'async_function' executed in" in captured.out