import pytest


@pytest.mark.asyncio
async def test_metricas_incluye_tecnicas_y_auditoria(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    await client.post('/api/autenticacion/iniciar-sesion', json={'correo': 'admin@sistema.com', 'clave': 'Admin123!'})

    response = await client.get('/api/metricas', headers=headers)
    assert response.status_code == 200

    datos = response.json().get('datos', {})
    assert 'tecnicas' in datos
    assert 'auditoria' in datos
    assert 'conteo_eventos' in datos.get('auditoria', {})
