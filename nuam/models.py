from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)


class Registro(models.Model):
    """
    Registro principal de la UI_INGRESO_CALIFICACIONES_TRIBUTARIAS.
    Basado en las columnas del archivo de carga + factores 8 al 37.
    """

    # -----------------------------
    # CAMPOS GENERALES DEL ENCABEZADO
    # -----------------------------

    ejercicio = models.PositiveIntegerField(
        help_text="Ejercicio / Año. Ej: 2023",
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100),
        ],
    )

    mercado = models.CharField(
        max_length=3,
        help_text="Mercado (3 caracteres). Ej: ACN",
        validators=[
            RegexValidator(
                regex=r"^[A-Z0-9]{1,3}$",
                message="El mercado debe tener entre 1 y 3 caracteres en mayúscula.",
            )
        ],
    )

    instrumento = models.CharField(
        max_length=100,
        help_text="Instrumento. Ej: COPEC",
    )

    fecha_pago = models.DateField(
        help_text="Fecha de pago en formato DD-MM-AAAA",
    )

    secuencia_evento = models.CharField(
        max_length=10,
        help_text="Secuencia del evento (hasta 10 dígitos).",
        validators=[
            RegexValidator(
                regex=r"^[0-9]{1,10}$",
                message="La secuencia debe contener solo dígitos (máx. 10).",
            )
        ],
    )

    numero_dividendo = models.CharField(
        max_length=10,
        help_text="Número de dividendo (hasta 10 dígitos).",
        validators=[
            RegexValidator(
                regex=r"^[0-9]{1,10}$",
                message="El número de dividendo debe contener solo dígitos (máx. 10).",
            )
        ],
        blank=True,
        null=True,
    )

    # Tipo de sociedad
    TIPO_SOCIEDAD_CHOICES = [
        ("SAA", "Sociedad Anónima Abierta (S.A. Abierta)"),
        ("SAC", "Sociedad Anónima Cerrada (S.A. Cerrada)"),
        ("SPA", "Sociedad por Acciones (SpA)"),
        ("LTDA", "Sociedad de Responsabilidad Limitada (Ltda.)"),
        ("EIRL", "Empresa Individual de Responsabilidad Limitada (EIRL)"),
        ("EXT", "Sociedad Extranjera"),
        ("OTRA", "Otra entidad / vehículo de inversión"),
    ]

    tipo_sociedad = models.CharField(
        max_length=4,
        choices=TIPO_SOCIEDAD_CHOICES,
        help_text="Tipo de sociedad emisora responsable del instrumento.",
    )

    # =============================
    # EVENTO DE CAPITAL (EMPRESARIAL)
    # =============================
    TIPO_EVENTO_CAPITAL_CHOICES = [
        ("AUM_CAP", "Aumento de capital"),
        ("DIS_CAP", "Disminución de capital"),
        ("DIV_CAP", "Distribución de dividendos"),
        ("FUSION", "Fusión / Reorganización societaria"),
        ("OTRO", "Otro evento de capital"),
    ]

    tipo_evento_capital = models.CharField(
        verbose_name="Tipo de evento de capital",
        max_length=20,
        choices=TIPO_EVENTO_CAPITAL_CHOICES,
        blank=True,
        null=True,
        help_text="Clasificación del evento de capital asociado al instrumento.",
    )

    monto_evento_capital = models.DecimalField(
        verbose_name="Monto asociado al evento de capital",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0"))],
        help_text=(
            "Monto monetario vinculado al evento de capital "
            "(por ejemplo, emisión, disminución o distribución de capital)."
        ),
    )

    valor_historico = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        help_text="Valor histórico (entero, hasta 10 dígitos).",
        validators=[
            MinValueValidator(0),
        ],
    )

    descripcion = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Descripción opcional del evento / instrumento.",
    )

    # =============================
    # NUEVO CAMPO ISUF
    # =============================
    isuf = models.BooleanField(
        default=False,
        help_text="Indica si la operación tiene tratamiento ISUF (Sí/No)."
    )

    calificacion_tributaria = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
        help_text="Calificación tributaria entre 1.0 y 7.0.",
        validators=[
            MinValueValidator(Decimal("1.0")),
            MaxValueValidator(Decimal("7.0")),
        ],
    )

    # -----------------------------
    # FACTORES 8 AL 37
    # -----------------------------
    def _factor_field(help_text):
        # IMPORTANTE: ahora el máximo es 1.00000000 (no puede ser mayor que 1)
        return models.DecimalField(
            max_digits=10,          # 1 entero + 8 decimales
            decimal_places=8,
            null=True,
            blank=True,
            validators=[
                MinValueValidator(Decimal("0")),
                MaxValueValidator(Decimal("1.00000000")),
            ],
            help_text=help_text,
        )

    factor_8 = _factor_field("Factor 8: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_9 = _factor_field("Factor 9: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_10 = _factor_field("Factor 10: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_11 = _factor_field("Factor 11: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_12 = _factor_field("Factor 12: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_13 = _factor_field("Factor 13: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_14 = _factor_field("Factor 14: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_15 = _factor_field("Factor 15: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_16 = _factor_field("Factor 16: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_17 = _factor_field("Factor 17: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_18 = _factor_field("Factor 18: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_19 = _factor_field("Factor 19: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_20 = _factor_field("Factor 20: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_21 = _factor_field("Factor 21: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_22 = _factor_field("Factor 22: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_23 = _factor_field("Factor 23: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_24 = _factor_field("Factor 24: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_25 = _factor_field("Factor 25: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_26 = _factor_field("Factor 26: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_27 = _factor_field("Factor 27: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_28 = _factor_field("Factor 28: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_29 = _factor_field("Factor 29: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_30 = _factor_field("Factor 30: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_31 = _factor_field("Factor 31: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_32 = _factor_field("Factor 32: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_33 = _factor_field("Factor 33: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_34 = _factor_field("Factor 34: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_35 = _factor_field("Factor 35: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_36 = _factor_field("Factor 36: decimal entre 0 y 1, con hasta 8 decimales.")
    factor_37 = _factor_field("Factor 37: decimal entre 0 y 1, con hasta 8 decimales.")

    # -----------------------------
    # METADATOS
    # -----------------------------
    usuario_registro = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="registros_calificacion",
        help_text="Usuario NUAM que realiza el ingreso o modificación.",
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Registro de Calificación Tributaria"
        verbose_name_plural = "Registros de Calificación Tributaria"
        ordering = ["-fecha_pago", "-fecha_creacion"]

    def __str__(self):
        return f"{self.ejercicio} - {self.mercado} - {self.instrumento}"


# =========================
# LOGIN ATTEMPT (AUDITORÍA)
# =========================
class LoginAttempt(models.Model):

    username = models.CharField(
        max_length=150,
        help_text="Usuario ingresado en el formulario de login.",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Usuario autenticado (si el login fue exitoso).",
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP desde donde se hizo el intento.",
    )

    user_agent = models.TextField(
        blank=True,
        help_text="Navegador / dispositivo del cliente.",
    )

    successful = models.BooleanField(
        help_text="¿El intento fue exitoso?"
    )

    error_message = models.TextField(
        blank=True,
        help_text="Mensaje de error retornado (si aplica).",
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora del intento.",
    )

    class Meta:
        verbose_name = "Intento de inicio de sesión"
        verbose_name_plural = "Intentos de inicio de sesión"
        ordering = ["-timestamp"]

    def __str__(self):
        estado = "OK" if self.successful else "ERROR"
        return f"[{estado}] {self.username} @ {self.timestamp}"
