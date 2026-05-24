# Setup rapido

```bash
docker run --name fast-api-arq -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=fast-api-db -p 5432:5432 -d postgres:15-alpine
python -m pip install -r requirements.txt
```

## Levantar API

```bash
uvicorn main:app --reload
```

## Ejecutar pruebas

```bash
python -m pytest -q
```

## Limpieza de refresh tokens

### Modo app unica (default)

```env
LIMPIEZA_TOKENS_EN_API=true
```

### Modo distribuido (recomendado con multiples replicas)

1. Configura en `.env`:

```env
LIMPIEZA_TOKENS_EN_API=false
```

2. Programa este job (cron/worker) cada X horas:

```bash
python scripts/limpieza_tokens_refresco.py
```

## Troubleshooting

- Si falla al iniciar por `JWT_SECRET_KEY`, define una clave de 32+ caracteres en `.env`.
- Si falla conexion a DB, valida que el contenedor postgres este arriba y `DATABASE_URL` sea correcta.
- Si el puerto 5432 esta ocupado, cambia el mapeo del contenedor o usa una instancia local existente.
