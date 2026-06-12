import json
from pathlib import Path

from main import app


def test_contrato_openapi_congelado_v1():
    ruta = Path('tests/contrato_openapi_v1.json')
    assert ruta.exists(), 'No existe el contrato OpenAPI congelado.'

    esperado = json.loads(ruta.read_text(encoding='utf-8'))
    actual = app.openapi()

    # Comparacion estructural completa del contrato.
    assert actual == esperado


def test_contrato_openapi_rutas_criticas_presentes():
    rutas = app.openapi().get('paths', {})

    criticas = [
        '/api/autenticacion/iniciar-sesion',
        '/api/usuarios',
    ]

    for ruta in criticas:
        assert ruta in rutas, f'Falta ruta critica en contrato: {ruta}'
