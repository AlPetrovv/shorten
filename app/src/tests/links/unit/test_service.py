import pytest
from httpx import Response

pytestmark = pytest.mark.anyio


@pytestmark
async def test_create_short_link(api_client, mock_link_in):
    link_in = mock_link_in()
    response = await api_client.post("/links/shorten", json=link_in.model_dump(mode="json"))
    assert response.status_code == 201


@pytest.mark.parametrize(
    "source_link",
    [
        "https://www.youtube.com/",
        "https://www.facebook.com/",
    ],
)
async def test_create_status_code(api_client, mock_link_in, source_link):
    link_in = mock_link_in({"source_link": source_link})
    first_response = await api_client.post("/links/shorten", json=link_in.model_dump(mode="json"))
    assert first_response.status_code == 201
    second_response = await api_client.post("/links/shorten", json=link_in.model_dump(mode="json"))
    assert second_response.status_code == 200


@pytestmark
async def redirect(api_client, mock_link_in):
    link_in = mock_link_in()
    create_shorten_link_response: Response = await api_client.post(
        "/links/shorten",
        json=link_in.model_dump(mode="json"),
    )
    payload = create_shorten_link_response.json()
    assert "code" in payload
    redirect_response: Response = await api_client.get(f"links/{payload["code"]}")
    assert redirect_response.status_code == 301
