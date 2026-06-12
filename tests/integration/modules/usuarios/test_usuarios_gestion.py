import time

import pytest


@pytest.mark.asyncio
async def test_usuarios_gestion_requiere_token(client):
    response = await client.get('/api/usuarios')
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_usuarios_gestion_denegado_para_no_admin(client):
    login = await client.post('/api/autenticacion/iniciar-sesion', json={'correo': 'usuario@demo.com', 'clave': 'Admin123!'})
    token = login.json().get('datos', {}).get('token_acceso')
    response = await client.get('/api/usuarios', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_usuarios_gestion_crud_basico_admin(client, auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    correo_unico = f'gestion.usuario.{time.time_ns()}@demo.com'

    payload_crear = {
        'nombre': 'Gestion',
        'apellidos': 'Usuario',
        'correo': correo_unico,
        'telefono': '+51911111111',
        'foto_url': None,
        'rol_id': 2,
        'estado': 1,
    }
    r_crear = await client.post('/api/usuarios', json=payload_crear, headers=headers)
    assert r_crear.status_code == 201
    usuario_id = r_crear.json()['datos']['id']

    r_listar = await client.get('/api/usuarios?pagina=1&tamano=10&correo=gestion.usuario', headers=headers)
    assert r_listar.status_code == 200
    assert r_listar.json()['datos']['total'] >= 1

    r_detalle = await client.get(f'/api/usuarios/{usuario_id}', headers=headers)
    assert r_detalle.status_code == 200

    payload_actualizar = {
        'nombre': 'Gestionado',
        'apellidos': 'Actualizado',
        'correo': correo_unico,
        'telefono': '+51922222222',
        'foto_url': None,
        'rol_id': 2,
        'estado': 1,
    }
    r_update = await client.put(f'/api/usuarios/{usuario_id}', json=payload_actualizar, headers=headers)
    assert r_update.status_code == 200

    r_estado = await client.patch(f'/api/usuarios/{usuario_id}/estado', json={'estado': 0}, headers=headers)
    assert r_estado.status_code == 200
    assert r_estado.json()['datos']['estado'] == 0

    r_delete = await client.delete(f'/api/usuarios/{usuario_id}', headers=headers)
    assert r_delete.status_code == 200


@pytest.mark.asyncio
async def test_usuarios_gestion_validacion_payload(client, auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    payload_invalido = {
        'nombre': '',
        'apellidos': '',
        'correo': 'invalido',
        'rol_id': 999,
        'estado': 3,
    }
    response = await client.post('/api/usuarios', json=payload_invalido, headers=headers)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_usuarios_gestion_metodo_no_permitido(client, auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = await client.patch('/api/usuarios', json={}, headers=headers)
    assert response.status_code == 405


@pytest.mark.asyncio
async def test_usuarios_gestion_no_autodesactivar_admin(client, auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = await client.patch('/api/usuarios/1/estado', json={'estado': 0}, headers=headers)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_usuarios_gestion_correo_duplicado(client, auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    payload = {
        'nombre': 'Duplicado',
        'apellidos': 'Correo',
        'correo': 'admin@sistema.com',
        'telefono': '+51933333333',
        'foto_url': None,
        'rol_id': 2,
        'estado': 1,
    }
    response = await client.post('/api/usuarios', json=payload, headers=headers)
    assert response.status_code == 400
