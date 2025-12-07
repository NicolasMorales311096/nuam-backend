from decimal import Decimal
from datetime import datetime, timedelta
import pandas as pd

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Registro, LoginAttempt


# ============================
# Función auxiliar: IP cliente
# ============================
def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


# ============================
# INDEX
# ============================
def index(request):
    return render(request, "index.html")


# ============================
# LOGIN
# ============================
def login_view(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            error = "Debe llenar usuario y contraseña para iniciar sesión."
            return render(request, "login.html", {"error": error})

        ip = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        hace_10_min = timezone.now() - timedelta(minutes=10)
        intentos_fallidos = LoginAttempt.objects.filter(
            username=username,
            successful=False,
            timestamp__gte=hace_10_min,
        ).count()

        if intentos_fallidos >= 3:
            LoginAttempt.objects.create(
                username=username,
                user=None,
                ip_address=ip,
                user_agent=user_agent,
                successful=False,
                error_message="Cuenta bloqueada temporalmente por intentos fallidos.",
            )
            error = "Tu cuenta está bloqueada temporalmente por intentos fallidos. Intenta más tarde."
            return render(request, "login.html", {"error": error})

        user = authenticate(request, username=username, password=password)

        if user:
            LoginAttempt.objects.create(
                username=username,
                user=user,
                ip_address=ip,
                user_agent=user_agent,
                successful=True,
                error_message="",
            )
            login(request, user)
            return redirect("calcular")
        else:
            LoginAttempt.objects.create(
                username=username,
                user=None,
                ip_address=ip,
                user_agent=user_agent,
                successful=False,
                error_message="Usuario o contraseña incorrectos",
            )
            error = "Usuario o contraseña incorrectos."

    return render(request, "login.html", {"error": error})


# ============================
# LOGOUT
# ============================
def logout_view(request):
    if request.user.is_authenticated:
        ip = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        LoginAttempt.objects.create(
            username=request.user.username,
            user=request.user,
            ip_address=ip,
            user_agent=user_agent,
            successful=True,
            error_message="Cierre de sesión",
        )

    logout(request)
    return redirect("login")


# ============================
# PANEL CALCULAR
# ============================
@login_required(login_url="login")
def calcular_view(request):
    # Filtros desde la URL
    mercado_filtro = request.GET.get("mercado", "").strip().upper()
    isuf_filtro = request.GET.get("isuf", "").strip().upper()

    registros = Registro.objects.all().order_by("-fecha_pago", "-id")

    # --- Filtro por mercado ---
    if mercado_filtro and mercado_filtro != "TODOS":
        registros = registros.filter(mercado__iexact=mercado_filtro)
    else:
        mercado_filtro = "TODOS"

    # --- Filtro por ISUF (Sí / No / Todos) ---
    if isuf_filtro == "SI":
        registros = registros.filter(isuf=True)
    elif isuf_filtro == "NO":
        registros = registros.filter(isuf=False)
    else:
        isuf_filtro = "TODOS"

    total_registros = registros.count()

    promedio_calificacion = None
    if registros.exists():
        califs = [r.calificacion_tributaria for r in registros if r.calificacion_tributaria is not None]
        if califs:
            promedio_calificacion = round(float(sum(califs)) / len(califs), 2)

    return render(request, "calcular.html", {
        "registros": registros,
        "mercado_filtro": mercado_filtro,
        "isuf_filtro": isuf_filtro,          # 👈 importante para el combo ISUF en el template
        "total_registros": total_registros,
        "promedio_calificacion": promedio_calificacion,
    })


# ============================
# INSERTAR REGISTRO
# ============================
@login_required(login_url="login")
def insertar_view(request):
    error = ""
    mensaje = ""
    form_data = {}
    factors_range = range(8, 38)

    if request.method == "POST":
        campos = [
            "ejercicio", "mercado", "instrumento", "fecha_pago",
            "secuencia_evento", "numero_dividendo", "tipo_sociedad",
            "tipo_evento_capital", "monto_evento_capital",
            "valor_historico", "descripcion", "calificacion_tributaria",
            "isuf",
        ] + [f"factor_{i}" for i in factors_range]

        for c in campos:
            form_data[c] = request.POST.get(c, "").strip()

        try:
            if not form_data["ejercicio"]:
                raise ValueError("Debe ingresar el ejercicio.")
            if not form_data["mercado"]:
                raise ValueError("Debe ingresar el mercado.")
            if not form_data["instrumento"]:
                raise ValueError("Debe ingresar el instrumento.")
            if not form_data["fecha_pago"]:
                raise ValueError("Debe ingresar la fecha de pago.")
            if not form_data["secuencia_evento"]:
                raise ValueError("Debe ingresar la secuencia del evento.")
            if not form_data["tipo_sociedad"]:
                raise ValueError("Debe seleccionar el tipo de sociedad.")
            if not form_data["valor_historico"]:
                raise ValueError("Debe ingresar el valor histórico.")

            # Checkbox ISUF
            isuf = True if request.POST.get("isuf") == "on" else False

            factores = {}
            valores_factores_ingresados = []

            for i in factors_range:
                key = f"factor_{i}"
                val_str = form_data.get(key, "").strip()

                if val_str:
                    factor_decimal = Decimal(val_str)
                    valor_normalizado = str(factor_decimal.normalize())

                    if valor_normalizado in valores_factores_ingresados:
                        raise ValueError(
                            f"El valor de factor '{val_str}' está repetido. Todos los factores deben ser únicos."
                        )

                    valores_factores_ingresados.append(valor_normalizado)
                    factores[key] = factor_decimal
                else:
                    factores[key] = None

            ejercicio = int(form_data["ejercicio"])
            mercado = form_data["mercado"].upper()
            instrumento = form_data["instrumento"]
            fecha_pago = datetime.strptime(form_data["fecha_pago"], "%Y-%m-%d").date()
            secuencia_evento = form_data["secuencia_evento"]
            numero_dividendo = form_data["numero_dividendo"] or None
            tipo_sociedad = form_data["tipo_sociedad"]

            tipo_evento_capital = form_data.get("tipo_evento_capital") or None

            monto_evento_capital_str = form_data.get("monto_evento_capital", "").replace(",", ".")
            monto_evento_capital = Decimal(monto_evento_capital_str) if monto_evento_capital_str else None

            valor_historico = Decimal(form_data["valor_historico"])
            descripcion = form_data["descripcion"] or None

            calif_str = form_data["calificacion_tributaria"]
            calificacion_tributaria = Decimal(calif_str) if calif_str else None

            registro = Registro(
                ejercicio=ejercicio,
                mercado=mercado,
                instrumento=instrumento,
                fecha_pago=fecha_pago,
                secuencia_evento=secuencia_evento,
                numero_dividendo=numero_dividendo,
                tipo_sociedad=tipo_sociedad,
                tipo_evento_capital=tipo_evento_capital,
                monto_evento_capital=monto_evento_capital,
                valor_historico=valor_historico,
                descripcion=descripcion,
                calificacion_tributaria=calificacion_tributaria,
                isuf=isuf,
                usuario_registro=request.user,
                **factores
            )

            registro.full_clean()
            registro.save()
            mensaje = "Registro ingresado correctamente."
            form_data = {}

        except Exception as e:
            error = f"Error al guardar el registro: {e}"

    registros = Registro.objects.all().order_by("-fecha_creacion")[:10]

    return render(request, "insertar.html", {
        "error": error,
        "mensaje": mensaje,
        "form_data": form_data,
        "registros": registros,
        "factors_range": factors_range,
    })


# ============================
# ELIMINAR REGISTRO
# ============================
@login_required(login_url="login")
def eliminar_view(request):
    registros = Registro.objects.all().order_by("-fecha_creacion")[:20]
    mensaje = ""
    error = ""

    if request.user.username not in ["admin", "admin2"]:
        error = "Solo los usuarios admin y admin2 tienen privilegios para eliminar."
        return render(request, "eliminar.html", {
            "registros": registros,
            "mensaje": mensaje,
            "error": error,
        })

    if request.method == "POST":
        registro_id = request.POST.get("registro_id", "").strip()

        if not registro_id:
            error = "Debe ingresar un ID para eliminar."
        else:
            try:
                r = Registro.objects.get(id=registro_id)
                r.delete()
                mensaje = f"Registro ID {registro_id} eliminado correctamente."
            except Registro.DoesNotExist:
                error = f"No existe un registro con ID {registro_id}."

    return render(request, "eliminar.html", {
        "registros": registros,
        "mensaje": mensaje,
        "error": error,
    })


# ============================
# MODIFICAR REGISTRO
# ============================
@login_required(login_url="login")
def modificar_view(request, registro_id):

    if request.user.username not in ["admin", "admin2"]:
        return render(request, "modificar.html", {
            "error": "No tienes permisos para modificar. Solo admin y admin2.",
            "registro": None,
            "mensaje": "",
        })

    registro = get_object_or_404(Registro, id=registro_id)
    error = ""
    mensaje = ""
    factors_range = range(8, 38)

    if request.method == "POST":
        try:
            registro.ejercicio = int(request.POST.get("ejercicio", registro.ejercicio))
            registro.mercado = request.POST.get("mercado", registro.mercado).upper()
            registro.instrumento = request.POST.get("instrumento", registro.instrumento)

            fecha_pago_str = request.POST.get(
                "fecha_pago", registro.fecha_pago.strftime("%Y-%m-%d")
            )
            registro.fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d").date()

            registro.secuencia_evento = request.POST.get("secuencia_evento", registro.secuencia_evento)
            registro.numero_dividendo = request.POST.get("numero_dividendo", registro.numero_dividendo)
            registro.tipo_sociedad = request.POST.get("tipo_sociedad", registro.tipo_sociedad)

            # Evento de capital
            registro.tipo_evento_capital = request.POST.get("tipo_evento_capital") or None

            monto_cap_str = request.POST.get("monto_evento_capital", "").strip().replace(",", ".")
            registro.monto_evento_capital = Decimal(monto_cap_str) if monto_cap_str else None

            valor_historico_str = request.POST.get("valor_historico", str(registro.valor_historico))
            registro.valor_historico = Decimal(valor_historico_str)

            registro.descripcion = request.POST.get("descripcion", registro.descripcion)

            calif_str = request.POST.get("calificacion_tributaria", str(registro.calificacion_tributaria or "")).strip()
            registro.calificacion_tributaria = Decimal(calif_str) if calif_str else None

            # ISUF
            registro.isuf = True if request.POST.get("isuf") == "on" else False

            valores_factores_modificados = []

            for i in factors_range:
                key = f"factor_{i}"
                val_str = request.POST.get(key, "").strip()

                if val_str:
                    factor_decimal = Decimal(val_str)
                    valor_normalizado = str(factor_decimal.normalize())

                    if valor_normalizado in valores_factores_modificados:
                        raise ValueError(
                            f"El valor de factor '{val_str}' está repetido. Todos los factores deben ser únicos."
                        )

                    valores_factores_modificados.append(valor_normalizado)
                    setattr(registro, key, factor_decimal)
                else:
                    setattr(registro, key, None)

            registro.full_clean()
            registro.save()
            mensaje = "Registro modificado correctamente."

        except Exception as e:
            error = f"Error al modificar el registro: {e}"

    factores = [{"numero": i, "valor": getattr(registro, f"factor_{i}", None)}
                for i in factors_range]

    return render(request, "modificar.html", {
        "registro": registro,
        "error": error,
        "mensaje": mensaje,
        "factores": factores,
    })


# ============================
# CARGAR ARCHIVO REAL (CSV/XLSX)
# ============================
@login_required(login_url="login")
def cargar_archivo_view(request):
    mensaje = ""
    error = ""
    nombre_archivo = ""
    size_archivo = None
    creados = 0
    errores = []

    if request.method == "POST":
        archivo = request.FILES.get("archivo")

        if not archivo:
            error = "Debe seleccionar un archivo."
        else:
            nombre_archivo = archivo.name
            size_archivo = archivo.size

            # Validación extensión
            if not nombre_archivo.lower().endswith((".csv", ".xlsx")):
                error = "El archivo debe ser .csv o .xlsx"
            else:
                # Cargar archivo
                try:
                    if nombre_archivo.lower().endswith(".csv"):
                        df = pd.read_csv(archivo, dtype=str)
                    else:
                        df = pd.read_excel(archivo, dtype=str)
                except Exception:
                    error = "El archivo no se pudo leer. Verifique el formato."
                    df = None

                if df is not None:

                    df.columns = [c.strip().lower() for c in df.columns]

                    columnas_obligatorias = [
                        "ejercicio", "mercado", "instrumento", "fecha_pago",
                        "secuencia_evento", "tipo_sociedad",
                        "valor_historico", "calificacion_tributaria",
                        "isuf",
                    ] + [f"factor_{i}" for i in range(8, 38)]

                    for col in columnas_obligatorias:
                        if col not in df.columns:
                            error = f"Falta la columna obligatoria: {col}"
                            return render(request, "cargar_archivo.html", {
                                "mensaje": mensaje,
                                "error": error,
                                "nombre_archivo": nombre_archivo,
                                "size_archivo": size_archivo,
                                "creados": creados,
                                "errores": errores,
                            })

                    fila_num = 1

                    for idx, fila in df.iterrows():
                        fila_num += 1
                        try:
                            ejercicio = int(fila["ejercicio"])
                            mercado = str(fila["mercado"]).upper().strip()
                            instrumento = str(fila["instrumento"]).strip()

                            # Fecha DD-MM-YYYY
                            fecha = str(fila["fecha_pago"]).strip()
                            fecha_pago = datetime.strptime(fecha, "%d-%m-%Y").date()

                            secuencia_evento = str(fila["secuencia_evento"]).strip()
                            numero_dividendo = (
                                str(fila["numero_dividendo"]).strip()
                                if "numero_dividendo" in fila and pd.notna(fila["numero_dividendo"])
                                else None
                            )

                            tipo_sociedad = str(fila["tipo_sociedad"]).strip()

                            tipo_evento_capital = (
                                str(fila["tipo_evento_capital"]).strip()
                                if "tipo_evento_capital" in fila
                                else None
                            )

                            monto_evento_capital = (
                                Decimal(str(fila["monto_evento_capital"]).replace(",", "."))
                                if "monto_evento_capital" in fila and pd.notna(fila["monto_evento_capital"])
                                else None
                            )

                            valor_historico = Decimal(str(fila["valor_historico"]))
                            descripcion = (
                                str(fila["descripcion"]).strip()
                                if "descripcion" in fila and pd.notna(fila["descripcion"])
                                else None
                            )

                            calificacion_tributaria = (
                                Decimal(str(fila["calificacion_tributaria"]))
                                if pd.notna(fila["calificacion_tributaria"])
                                else None
                            )

                            # ISUF
                            isuf_val = str(fila["isuf"]).strip()
                            if isuf_val not in ["0", "1"]:
                                raise ValueError("ISUF debe ser 1 o 0")
                            isuf = True if isuf_val == "1" else False

                            # FACTORES
                            factores = {}
                            valores_norm = []

                            for i in range(8, 38):
                                key = f"factor_{i}"
                                raw_val = fila[key]

                                if pd.isna(raw_val) or raw_val == "":
                                    factores[key] = None
                                else:
                                    val = Decimal(str(raw_val))
                                    norm = str(val.normalize())
                                    if norm in valores_norm:
                                        raise ValueError(f"Factor repetido en F{i}")
                                    valores_norm.append(norm)
                                    factores[key] = val

                            registro = Registro(
                                ejercicio=ejercicio,
                                mercado=mercado,
                                instrumento=instrumento,
                                fecha_pago=fecha_pago,
                                secuencia_evento=secuencia_evento,
                                numero_dividendo=numero_dividendo,
                                tipo_sociedad=tipo_sociedad,
                                tipo_evento_capital=tipo_evento_capital,
                                monto_evento_capital=monto_evento_capital,
                                valor_historico=valor_historico,
                                descripcion=descripcion,
                                calificacion_tributaria=calificacion_tributaria,
                                isuf=isuf,
                                usuario_registro=request.user,
                                **factores
                            )

                            registro.full_clean()
                            registro.save()
                            creados += 1

                        except Exception as e:
                            errores.append(f"Fila {fila_num}: {e}")

                    mensaje = f"Carga completada. Registros creados: {creados}"

    return render(request, "cargar_archivo.html", {
        "mensaje": mensaje,
        "error": error,
        "nombre_archivo": nombre_archivo,
        "size_archivo": size_archivo,
        "creados": creados,
        "errores": errores,
    })


# ============================
# AUDITORÍA
# ============================
@login_required(login_url="login")
def auditoria_view(request):
    if request.user.username not in ["admin", "admin2"]:
        return render(request, "auditoria.html", {
            "mensaje": "No tienes permisos para ver la auditoría.",
            "intentos": [],
            "registros": [],
        })

    intentos = LoginAttempt.objects.all().order_by("-timestamp")[:100]
    registros = Registro.objects.all().order_by("-fecha_creacion")[:50]

    return render(request, "auditoria.html", {
        "mensaje": "",
        "intentos": intentos,
        "registros": registros,
    })
