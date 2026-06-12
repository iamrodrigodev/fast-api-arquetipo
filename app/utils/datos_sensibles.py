import re


def enmascarar_correo(correo: str | None) -> str:
    if not correo:
        return "<sin_correo>"
    if "@" not in correo:
        return "***"
    usuario, dominio = correo.split("@", 1)
    if len(usuario) <= 2:
        usuario_mask = "*" * len(usuario)
    else:
        usuario_mask = usuario[0] + ("*" * (len(usuario) - 2)) + usuario[-1]
    return f"{usuario_mask}@{dominio}"


def enmascarar_telefono(telefono: str | None) -> str:
    if not telefono:
        return "<sin_telefono>"
    digitos = re.sub(r"\D", "", telefono)
    if len(digitos) <= 4:
        return "*" * len(digitos)
    return ("*" * (len(digitos) - 4)) + digitos[-4:]


def enmascarar_documento(documento: str | None) -> str:
    if not documento:
        return "<sin_documento>"
    limpio = documento.strip()
    if len(limpio) <= 3:
        return "*" * len(limpio)
    return limpio[0:2] + ("*" * (len(limpio) - 3)) + limpio[-1]


def sanitizar_campos_sensibles(datos: dict) -> dict:
    resultado = {}
    for clave, valor in datos.items():
        clave_l = clave.lower()
        if "correo" in clave_l:
            resultado[clave] = enmascarar_correo(str(valor) if valor is not None else None)
        elif "telefono" in clave_l:
            resultado[clave] = enmascarar_telefono(str(valor) if valor is not None else None)
        elif "documento" in clave_l:
            resultado[clave] = enmascarar_documento(str(valor) if valor is not None else None)
        else:
            resultado[clave] = valor
    return resultado
