from http import HTTPStatus


def test_get_games(client):
    response = client.get(
        '/games/?offset=2'
    )

    assert response.status_code == HTTPStatus.OK
