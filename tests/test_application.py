import pytest
from faststream.kafka import TestKafkaBroker
from fastapi.testclient import TestClient

from app.application import Name, router, app

client = TestClient(app)

@router.broker.subscriber("names")
async def on_names(msg: Name) -> None:
    pass


@pytest.mark.asyncio
async def test_on_names():
    async with TestKafkaBroker(router.broker):
        response = client.post(
            "/name/",
            json={"name": "Tvrtko"},
        )
        assert response.status_code == 200
        on_names.mock.assert_called_with(dict(Name(name="Tvrtko")))