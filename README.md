docker run --name chequeo-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=chequeo_accion_plena_db -p 5432:5432 -d postgres:15-alpine


uvicorn main:app --reload