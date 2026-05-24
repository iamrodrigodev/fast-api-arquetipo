import pytest


@pytest.mark.asyncio
async def test_perfil_sin_token(client):
    response = await client.get('/api/usuario/perfil')
    body = response.json()

    assert response.status_code == 401
    assert body.get('estado') == 401
    assert body.get('mensaje') == 'No autorizado'


@pytest.mark.asyncio
async def test_perfil_token_invalido(client):
    response = await client.get('/api/usuario/perfil', headers={'Authorization': 'Bearer token.invalido'})
    body = response.json()

    assert response.status_code == 401
    assert body.get('estado') == 401
    assert body.get('mensaje') == 'No autorizado'


@pytest.mark.asyncio
async def test_perfil_token_valido(client, auth_token):
    response = await client.get('/api/usuario/perfil', headers={'Authorization': f'Bearer {auth_token}'})
    body = response.json()

    assert response.status_code == 200
    assert body.get('estado') == 200
    assert body.get('mensaje') == 'Datos obtenidos exitosamente'
    assert body.get('datos', {}).get('correo') == 'admin@sistema.com'


@pytest.mark.asyncio
async def test_perfil_por_id_admin_permitido(client, auth_token):
    response = await client.get('/api/usuario/1/perfil', headers={'Authorization': f'Bearer {auth_token}'})
    body = response.json()

    assert response.status_code == 200
    assert body.get('estado') == 200


@pytest.mark.asyncio
async def test_perfil_por_id_no_existente_admin(client, auth_token):
    response = await client.get('/api/usuario/999999/perfil', headers={'Authorization': f'Bearer {auth_token}'})
    body = response.json()

    assert response.status_code == 404
    assert body.get('estado') == 404


@pytest.mark.asyncio
async def test_perfil_por_id_usuario_no_admin_denegado(client):
    login_usuario = await client.post(
        '/api/autenticacion/iniciar-sesion',
        json={'correo': 'usuario@demo.com', 'clave': 'Admin123!'}
    )
    token_usuario = login_usuario.json().get('datos', {}).get('token_acceso')
    assert token_usuario

    response = await client.get('/api/usuario/1/perfil', headers={'Authorization': f'Bearer {token_usuario}'})
    body = response.json()

    assert response.status_code == 403
    assert body.get('estado') == 403


@pytest.mark.asyncio
async def test_perfil_usuario_inactivo_no_autorizado(client):
    login_admin = await client.post(
        '/api/autenticacion/iniciar-sesion',
        json={'correo': 'admin@sistema.com', 'clave': 'Admin123!'}
    )
    token_admin = login_admin.json().get('datos', {}).get('token_acceso')
    assert token_admin

    from app.modules.usuarios.repositories.usuario_repository import UsuarioRepository
    usuario = await UsuarioRepository.buscar_por_correo('usuario@demo.com')
    usuario.estado = 0
    await UsuarioRepository.guardar(usuario)

    try:
        login_usuario = await client.post(
            '/api/autenticacion/iniciar-sesion',
            json={'correo': 'usuario@demo.com', 'clave': 'Admin123!'}
        )
        token_usuario = login_usuario.json().get('datos', {}).get('token_acceso')
        assert token_usuario

        response = await client.get('/api/usuario/perfil', headers={'Authorization': f'Bearer {token_usuario}'})
        body = response.json()

        assert response.status_code == 401
        assert body.get('estado') == 401
    finally:
        usuario.estado = 1
        await UsuarioRepository.guardar(usuario)
