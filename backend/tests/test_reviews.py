from http import HTTPStatus


def test_create_review(client, user, token):
    response = client.post(
        '/reviews',
        json={
            'title': 'test',
            'text': 'test',
            'rating': 5,
            'game': 'test',
        }
    )

    assert response.status_code == HTTPStatus.OK


def test_get_review(client, user, authenticated, review):
    # this is as powerful as the world :D
    response = authenticated.get('/reviews')
    print(response.json())
    assert response.status_code == HTTPStatus.OK
    assert response.json()[0] == {
        'id': review.id,
        'user_id': user.id,
        'title': review.title,
        'text': review.text,
        'game': review.game,
        'rating': review.rating,
    }
