# Setup rapido

docker run --name chequeo-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=chequeo_accion_plena_db -p 5432:5432 -d postgres:15-alpine
python -m pip install -r requirements.txt

# Levantar API
uvicorn main:app --reload

# Ejecutar pruebas
python -m pytest -q

# Limpieza de refresh tokens
# Modo app unica (default):
# LIMPIEZA_TOKENS_EN_API=true
#
# Modo distribuido (recomendado con multiples replicas):
# 1) Configura LIMPIEZA_TOKENS_EN_API=false en .env
# 2) Programa este job (cron/worker) cada X horas:
#    python scripts/limpieza_tokens_refresco.py

# Troubleshooting
- Si falla al iniciar por JWT_SECRET_KEY, define una clave de 32+ caracteres en .env.
- Si falla conexion a DB, valida que el contenedor postgres este arriba y DATABASE_URL sea correcta.
- Si el puerto 5432 esta ocupado, cambia el mapeo del contenedor o usa una instancia local existente.
