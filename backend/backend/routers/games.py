import json

from fastapi import APIRouter, Depends
from igdb.wrapper import IGDBWrapper

from backend.services import get_igdb_token
from backend.settings import Settings

router = APIRouter(prefix='/games', tags=['games'])


@router.get('/')
def get_games(
    api_token: str = Depends(get_igdb_token),
    offset: int = 10,
):
    wrapper = IGDBWrapper(Settings().IGDB_CLIENT_ID, api_token)

    byte_array_response = wrapper.api_request(
        'games',
        f'fields name, genres, release_dates; limit {offset};'
    )

    # Decode the byte array to a string
    json_str = byte_array_response.decode('utf-8')

    # Parse the JSON string to a python dictionary
    data = json.loads(json_str)

    print(data)
