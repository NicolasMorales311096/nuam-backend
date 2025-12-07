from django.contrib import admin
from .models import Registro, LoginAttempt


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    """
    Admin profesional para la UI_INGRESO_CALIFICACIONES_TRIBUTARIAS.
    Pensado para mostrar lo mismo que el mockup pero en versión interna.
    """

    # -----------------------------
    # LISTADO PRINCIPAL
    # -----------------------------
    list_display = (
        "ejercicio",
        "mercado",
        "instrumento",
        "fecha_pago",
        "tipo_sociedad",
        "valor_historico",
        "calificacion_tributaria",
        "usuario_registro",
        "fecha_creacion",
    )

    list_filter = (
        "ejercicio",
        "mercado",
        "tipo_sociedad",
        "usuario_registro",
        "fecha_pago",
        "fecha_creacion",
    )

    search_fields = (
        "instrumento",
        "descripcion",
        "mercado",
        "secuencia_evento",
        "numero_dividendo",
    )

    date_hierarchy = "fecha_pago"
    list_per_page = 25
    ordering = ("-fecha_pago", "-fecha_creacion")

    # -----------------------------
    # CAMPOS SOLO LECTURA
    # -----------------------------
    readonly_fields = (
        "fecha_creacion",
        "fecha_actualizacion",
    )

    # -----------------------------
    # ORGANIZACIÓN EN SECCIONES
    # -----------------------------
    fieldsets = (
        (
            "Datos generales",
            {
                "fields": (
                    "ejercicio",
                    "mercado",
                    "instrumento",
                    "fecha_pago",
                    "secuencia_evento",
                    "numero_dividendo",
                    "tipo_sociedad",
                    "valor_historico",
                )
            },
        ),
        (
            "Descripción y calificación",
            {
                "fields": (
                    "descripcion",
                    "calificacion_tributaria",
                )
            },
        ),
        (
            "Factores 8 al 20",
            {
                "classes": ("collapse",),
                "fields": (
                    "factor_8",
                    "factor_9",
                    "factor_10",
                    "factor_11",
                    "factor_12",
                    "factor_13",
                    "factor_14",
                    "factor_15",
                    "factor_16",
                    "factor_17",
                    "factor_18",
                    "factor_19",
                    "factor_20",
                ),
                "description": "Factores definidos con 1 entero y 8 decimales (según especificación del archivo de carga).",
            },
        ),
        (
            "Factores 21 al 37",
            {
                "classes": ("collapse",),
                "fields": (
                    "factor_21",
                    "factor_22",
                    "factor_23",
                    "factor_24",
                    "factor_25",
                    "factor_26",
                    "factor_27",
                    "factor_28",
                    "factor_29",
                    "factor_30",
                    "factor_31",
                    "factor_32",
                    "factor_33",
                    "factor_34",
                    "factor_35",
                    "factor_36",
                    "factor_37",
                ),
            },
        ),
        (
            "Trazabilidad",
            {
                "classes": ("collapse",),
                "fields": (
                    "usuario_registro",
                    "fecha_creacion",
                    "fecha_actualizacion",
                ),
            },
        ),
    )


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    """
    Admin para auditoría de intentos de inicio de sesión.
    Ideal para mostrar trazabilidad en la presentación.
    """

    list_display = (
        "username",
        "user",
        "successful",
        "ip_address",
        "timestamp",
    )

    list_filter = (
        "successful",
        "user",
        "timestamp",
    )

    search_fields = (
        "username",
        "ip_address",
        "user_agent",
    )

    readonly_fields = (
        "username",
        "user",
        "ip_address",
        "user_agent",
        "successful",
        "error_message",
        "timestamp",
    )

    date_hierarchy = "timestamp"
    list_per_page = 50
    ordering = ("-timestamp",)

    fieldsets = (
        (
            "Datos del intento",
            {
                "fields": (
                    "username",
                    "user",
                    "successful",
                    "error_message",
                )
            },
        ),
        (
            "Información técnica",
            {
                "classes": ("collapse",),
                "fields": (
                    "ip_address",
                    "user_agent",
                ),
            },
        ),
        (
            "Trazabilidad",
            {
                "fields": ("timestamp",),
            },
        ),
    )
