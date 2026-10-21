import pytest_asyncio
from httpx import ASGITransport, AsyncClient

import main
from main import app


@pytest_asyncio.fixture
async def client():
    main.tasks.clear()           # очищаем хранилище перед каждым тестом
    main.next_id = 1             # сбрасываем счётчик идентификаторов
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as c:
        yield c

@pytest_asyncio.fixture
async def sample_task(client):
    main.tasks.clear()  # очищаем хранилище перед каждым тестом
    main.next_id = 1
    response = await client.post('/tasks', json={"title": "sample", "description": "for tests"})
    return response.json()['id']