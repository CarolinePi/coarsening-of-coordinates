
async def test_healthcheck(client_without_login):
    resp = await client_without_login.get('/healthcheck')
    assert resp.status == 200
    text = await resp.text()
    assert 'I am fine!' in text


async def test_get_user_without_login(client_without_login, test_db):
    resp = await client_without_login.get('/user/1')
    assert resp.status == 200
    json = await resp.json()
    json_answer = {"id": 1, "full_name": "Caroline Pospelova", "location": {"latitude": "123.23733", "longitude": "87.33993"}}
    assert json == json_answer


async def test_get_user_with_login(client_with_login, test_db):
    resp = await client_with_login.get('/user/1')
    assert resp.status == 200
    json = await resp.json()
    json_answer = {"id": 1, "full_name": "Caroline Pospelova", "location": {"latitude": "123.23123", "longitude": "87.323"}}
    assert json == json_answer
