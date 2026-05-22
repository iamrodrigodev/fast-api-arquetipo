import uvicorn
from src.config.iniciador import IniciadorApp
from src.controller.enrutador import registrar_rutas
from src.exception.manejador_global import registrar_manejadores_error
from src.config.ajustes import ajustes

app = IniciadorApp.configurar()

registrar_rutas(app)
registrar_manejadores_error(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=ajustes.PUERTO, reload=True)
