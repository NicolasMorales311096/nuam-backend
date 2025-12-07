# app/utils_validaciones.py
from decimal import Decimal
import re
from django.core.exceptions import ValidationError

# ----- Validación de RUT chileno -----
def validar_rut(rut: str) -> bool:
    """
    Valida RUT chileno en formato 11111111-1 o 11.111.111-1.
    Devuelve True si es válido, False si no.
    """
    rut = rut.replace(".", "").replace("-", "").upper()
    if len(rut) < 2:
        return False

    cuerpo, dv = rut[:-1], rut[-1]

    if not cuerpo.isdigit():
        return False

    suma = 0
    multiplo = 2

    for digito in reversed(cuerpo):
        suma += int(digito) * multiplo
        multiplo += 1
        if multiplo == 8:
            multiplo = 2

    resto = suma % 11
    dv_calculado = 11 - resto
    if dv_calculado == 11:
        dv_calculado = "0"
    elif dv_calculado == 10:
        dv_calculado = "K"
    else:
        dv_calculado = str(dv_calculado)

    return dv_calculado == dv


def validar_mercado(mercado: str):
    """
    Debe ser 1 a 3 caracteres en mayúscula (ya lo reforzamos en el modelo).
    """
    if not re.match(r"^[A-Z0-9]{1,3}$", mercado or ""):
        raise ValidationError("Mercado debe tener entre 1 y 3 caracteres en mayúscula.")


def validar_factor(valor: Decimal, nombre: str):
    """
    Verifica que el factor tenga 1 entero y 8 decimales (0 a 9.99999999).
    """
    if valor is None:
        return
    if valor < Decimal("0") or valor > Decimal("9.99999999"):
        raise ValidationError(f"{nombre} debe estar entre 0 y 9.99999999.")
