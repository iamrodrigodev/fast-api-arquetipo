import pytest


@pytest.mark.asyncio
async def test_login_ok(client, login_payload_ok):
    response = await client.post('/api/autenticacion/iniciar-sesion', json=login_payload_ok)
    body = response.json()

    assert response.status_code == 200
    assert body.get('estado') == 200
    assert isinstance(body.get('mensaje'), str)
    assert isinstance(body.get('datos', {}).get('token_acceso'), str)
    assert isinstance(body.get('datos', {}).get('token_refresco'), str)


@pytest.mark.asyncio
async def test_login_bad_password(client, login_payload_bad):
    response = await client.post('/api/autenticacion/iniciar-sesion', json=login_payload_bad)
    body = response.json()

    assert response.status_code == 401
    assert body.get('estado') == 401
    assert isinstance(body.get('mensaje'), str)


@pytest.mark.asyncio
async def test_login_invalid_payload(client):
    response = await client.post('/api/autenticacion/iniciar-sesion', json={'correo': ''})
    body = response.json()

    assert response.status_code == 400
    assert body.get('estado') == 400
    assert isinstance(body.get('mensaje'), str)


@pytest.mark.asyncio
async def test_registro_duplicado(client):
    payload = {
        'nombre': 'Admin',
        'apellidos': 'Sistema',
        'correo': 'admin@sistema.com',
        'clave': 'Admin123!',
        'telefono': '999999999'
    }
    response = await client.post('/api/autenticacion/registrar-cuenta', json=payload)
    body = response.json()

    assert response.status_code == 400
    assert body.get('estado') == 400
    assert isinstance(body.get('mensaje'), str)


@pytest.mark.asyncio
async def test_refrescar_token_ok(client, token_refresco):
    response = await client.post('/api/autenticacion/refrescar-token', json={'token_refresco': token_refresco})
    body = response.json()

    assert response.status_code == 200
    assert body.get('estado') == 200
    assert isinstance(body.get('datos', {}).get('token_acceso'), str)
    assert isinstance(body.get('datos', {}).get('token_refresco'), str)


@pytest.mark.asyncio
async def test_cerrar_sesion_ok(client, token_refresco):
    response = await client.post('/api/autenticacion/cerrar-sesion', json={'token_refresco': token_refresco})
    body = response.json()

    assert response.status_code == 200
    assert body.get('estado') == 200
    assert isinstance(body.get('mensaje'), str)


@pytest.mark.asyncio
async def test_cerrar_sesion_todos_ok(client, auth_token):
    response = await client.post(
        '/api/autenticacion/cerrar-sesion-todos',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    body = response.json()

    assert response.status_code == 200
    assert body.get('estado') == 200
