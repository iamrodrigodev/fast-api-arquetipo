import pytest


@pytest.mark.asyncio
async def test_salud_ok(client):
    response = await client.get('/api/salud')
    body = response.json()

    assert response.status_code == 200
    assert body.get('estado') == 200
    assert body.get('mensaje') == 'Datos obtenidos exitosamente'
    assert isinstance(body.get('datos'), dict)
