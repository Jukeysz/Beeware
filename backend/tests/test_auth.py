from http import HTTPStatus

from freezegun import freeze_time


def test_login_token(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.plain_password,
        }
    )

    assert response.json() == {'message': 'login successful'}


def test_login_token_invalid_password(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': 'fandangos',
        }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_login_token_invalid_email(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': 'fandangos@fandango.com',
            'password': user.plain_password,
        }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_expired_token(client, user):
    with freeze_time('2024-06-25 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.plain_password}
        )
        assert response.status_code == HTTPStatus.OK
        cookies = response.cookies

    with freeze_time('2024-06-25 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            cookies=cookies,
            json={
                'username': 'fandangos',
                'email': 'fandangobom@fandango.com',
                'password': '12345',
            }
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh_token',
        cookies=token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'token refreshed'}


def test_refresh_token_with_expired_token(client, user):
    with freeze_time('2024-06-25 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.plain_password}
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'message': 'login successful'}
        cookies = response.cookies

    with freeze_time('2024-06-25 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            cookies=cookies,
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
