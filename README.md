# Beeware Project

## Resumo
Ainda em desenvolvimento, trata-se do meu projeto final do curso CS50 de harvard. Se tornará um website em que pessoas poderão criar seus guias junto à comunidades sobre jogos, além de tier lists e discussões de gameplay.

## Backend
Isso tudo só é possível graças à integração com a IGDB API da Twitch que gera responses sobre a base de dados dos jogos, assim tornando o meu trabalho mais trivial. A autenticação é feita com JWT Tokens que são implementados com httponly cookies, inacessíveis à ataques de scripting com Javascript.

- As tecnologias usadas foram FastAPI, SQLite, SQLAlchemy, Alembic(migrations) e Pytest.


## Frontend
A parte do cliente ainda está em desenvolvimento e em parte conceitual.
