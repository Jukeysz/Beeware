import json

from fastapi import APIRouter, Depends
from igdb.wrapper import IGDBWrapper

from backend.schemas import GameData
from backend.services import get_igdb_token
from backend.settings import Settings

router = APIRouter(prefix='/games', tags=['games'])
# session = Annotated[]...

# this endpoint will be useful for displaying a consecutive list of games
# divided
# by pages as the app's homepage

# I can implement a search input in the page that triggers another endpoint
# that uses query parameters for /search/games/{query}

# How about the specific game pages? they will use this very same endpoint,
# except that in this case it will have a single element by ID


@router.post('/')
async def get_games(
    game: GameData,
    offset: int = 10,
    api_token: str = Depends(get_igdb_token),
):
    wrapper = IGDBWrapper(Settings().IGDB_CLIENT_ID, api_token)

    # I will match the
    byte_array_response = wrapper.api_request(
        'games',
        f'fields id, name; where name ~ "{game.name}";'
    )

    # decode the byte array to a string
    json_str = byte_array_response.decode('utf-8')

    # parse the json string to a python dictionary
    data = json.loads(json_str)

    print(data)

    return data
