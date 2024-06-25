from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'test',
            'email': 'test@test.com',
            'password': '12345',
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'test',
        'email': 'test@test.com',
    }


def test_create_user_already_exists(client, user):
    response = client.post(
        '/users',
        json={
            'email': user.email,
            'username': user.username,
            'password': '12345',
        }
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_update_user_with_permission(client, token, user):
    response = client.put(
        f'/users/{user.id}',
        cookies=token,
        json={
            'username': 'joao123',
            'email': 'joao@joao.com',
            'password': '123456'
        }
    )

    assert response.status_code == HTTPStatus.OK


def test_update_user_without_permission(client, token, other_user):
    response = client.put(
        f'/users/{other_user.id}',
        cookies=token,
        json={
            'username': 'joao123',
            'email': 'joao@joao.com',
            'password': '123456'
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        'detail': 'user not authorized'
    }


def test_delete_user(client, token, user):
    response = client.delete(
        f'/users/{user.id}',
        cookies=token,
    )

    assert response.json() == {'message': 'User succesfully deleted'}
    assert response.status_code == HTTPStatus.OK


def test_delete_user_without_permission(client, token, other_user):
    response = client.delete(
        f'/users/{other_user.id}',
        cookies=token,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Invalid user id'}
