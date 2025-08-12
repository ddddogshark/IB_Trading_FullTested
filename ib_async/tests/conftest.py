import pytest
import asyncio

import ib_async as ibi


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    yield loop
    if not loop.is_closed():
        loop.close()


@pytest.fixture(scope="session")
async def ib():
    """IB连接fixture"""
    ib = ibi.IB()
    try:
        await ib.connectAsync('127.0.0.1', 4001, clientId=999, timeout=30)
        yield ib
    except Exception as e:
        print(f"连接失败: {e}")
        # 即使连接失败也返回ib实例，让测试可以继续
        yield ib
    finally:
        try:
            ib.disconnect()
        except:
            pass
