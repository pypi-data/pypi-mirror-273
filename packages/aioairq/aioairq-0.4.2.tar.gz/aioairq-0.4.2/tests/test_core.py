import aiohttp
import pytest
import pytest_asyncio
from pytest import fixture

from aioairq import AirQ


@fixture
def ip():
    return "192.168.0.0"


@fixture
def mdns():
    return "a123f_air-q.local"


@fixture
def passw():
    return "password"


@pytest_asyncio.fixture
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@fixture(params=["ip", "mdns"])
def valid_address(request, ip, mdns):
    return {"ip": ip, "mdns": mdns}[request.param]


@pytest.mark.asyncio
async def test_constructor(valid_address, passw, session):
    airq = AirQ(valid_address, passw, session)
    assert airq.anchor == "http://" + valid_address
    assert not airq._session.closed
