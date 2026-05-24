import os
import pytest
import pytest_asyncio
import httpx

os.environ.setdefault("JWT_SECRET_KEY", "jwt_secret_super_seguro_minimo_32_chars_ok")
os.environ.setdefault("CLAVE_SECRETA", "clave_interna_pruebas_segura_123456789")

from main import app


@pytest_asyncio.fixture(scope="session")
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture
def login_payload_ok():
    return {"correo": "admin@sistema.com", "clave": "Admin123!"}


@pytest.fixture
def login_payload_bad():
    return {"correo": "admin@sistema.com", "clave": "x"}


@pytest_asyncio.fixture
async def auth_token(client, login_payload_ok):
    response = await client.post("/api/autenticacion/iniciar-sesion", json=login_payload_ok)
    assert response.status_code == 200
    token = response.json().get("datos", {}).get("token_acceso")
    assert token
    return token


@pytest_asyncio.fixture
async def token_refresco(client, login_payload_ok):
    response = await client.post("/api/autenticacion/iniciar-sesion", json=login_payload_ok)
    assert response.status_code == 200
    token = response.json().get("datos", {}).get("token_refresco")
    assert token
    return token
