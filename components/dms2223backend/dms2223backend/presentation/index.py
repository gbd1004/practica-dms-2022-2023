from http import HTTPStatus

# NOTAS: ruta: '/'
#---------------------------------------------------
# La operación http HEAD no debe generar contenido,
# solo debe verificar que la API se esstá ejecutando
# (no es necesario devolver el 'header' tampoco).

def get_head() -> tuple[list, HTTPStatus]:
    return '', HTTPStatus.NOT_FOUND