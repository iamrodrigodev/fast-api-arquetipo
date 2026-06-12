from app.db.verificar_migraciones import verificar_revision_alembic


def test_smoke_verificador_migraciones_retorna_bool():
    resultado = verificar_revision_alembic()
    assert isinstance(resultado, bool)
