# models.py
from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

PT_NIF_REGEX = RegexValidator(regex=r"^\d{9}$", message="NIF must be 9 digits.")
PT_POSTAL_REGEX = RegexValidator(regex=r"^\d{4}-\d{3}$", message="Postal code must be NNNN-NNN.")
PHONE_REGEX = RegexValidator(regex=r"^[0-9+\-\s().]{7,20}$", message="Invalid phone number format.")

VIN_REGEX = RegexValidator(
    regex=r"^[A-HJ-NPR-Z0-9]{11,17}$",
    message="VIN must be 11–17 characters (alphanumeric, excluding I/O/Q)."
)
PLATE_REGEX = RegexValidator(
    regex=r"^[A-Z0-9\- ]{5,15}$",
    message="License plate should be 5–15 chars (letters/digits/hyphens/spaces)."
)

class Salesperson(models.Model):
    # Link to Django's built-in User
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="salesperson_profile",
        help_text="User account for this salesperson."
    )

    distributor = models.CharField(max_length=255, null=True, blank=True, db_column="DISTRIBUIDOR")
    active = models.BooleanField(default=True, db_column="ATIVO")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "salesperson"
        ordering = ["user__username"]
        indexes = [
            models.Index(fields=["distributor"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=6, unique=True, editable=False, db_column="Cliente_Codice")
    name = models.CharField(max_length=200, db_column="Cliente_Nome")

    nif = models.CharField(
        max_length=9, null=False, blank=False, unique=True, db_column="NIF",
        validators=[PT_NIF_REGEX],
        help_text="Portuguese taxpayer number (9 digits)."
    )
    address = models.CharField(max_length=255, null=True, blank=True, db_column="Morada")
    postal_code = models.CharField(
        max_length=8, null=True, blank=True, db_column="Cod_Postal",
        validators=[PT_POSTAL_REGEX],
    )
    city = models.CharField(max_length=120, null=True, blank=True, db_column="Localidade")

    phone = models.CharField(
        max_length=30, null=True, blank=True, db_column="Tel_geral",
        validators=[PHONE_REGEX],
    )
    email = models.EmailField(null=True, blank=True, db_column="Mail_geral")

    distributor = models.CharField(max_length=120, null=True, blank=True, db_column="Distribuidor")
    seller = models.CharField(max_length=120, null=True, blank=True, db_column="Vendedor")

    updated_at = models.DateTimeField(null=True, blank=True, db_column="Ultimo_Atualizar")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code and self.nif:
            self.code = self.nif[-6:]
        super().save(*args, **kwargs)

    class Meta:
        db_table = "client"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
            models.Index(fields=["nif"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class ClientContact(models.Model):
    id = models.BigAutoField(primary_key=True)

    client = models.ForeignKey(
        "Client",
        on_delete=models.CASCADE,
        related_name="contacts",
        db_index=True,
        help_text="Owning client."
    )

    name = models.CharField(max_length=200, help_text="Contact person name.")
    job_title = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(
        max_length=30, null=True, blank=True,
        validators=[PHONE_REGEX]
    )

    is_primary = models.BooleanField(default=False, help_text="Marks this as the primary contact for the client.")
    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "client_contact"
        verbose_name = "Client Contact"
        verbose_name_plural = "Client Contacts"
        ordering = ["client_id", "name"]
        indexes = [
            models.Index(fields=["client", "name"]),
            models.Index(fields=["client", "email"]),
            models.Index(fields=["client", "phone"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["client", "email"],
                name="uniq_client_contact_email",
                condition=models.Q(email__isnull=False),
            ),
            models.UniqueConstraint(
                fields=["client", "phone"],
                name="uniq_client_contact_phone",
                condition=models.Q(phone__isnull=False),
            ),
            models.UniqueConstraint(
                fields=["client", "is_primary"],
                name="uniq_client_primary_contact",
                condition=models.Q(is_primary=True),
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.client.name})"

class VP(models.Model):
    id = models.BigAutoField(primary_key=True)
    vp_code = models.CharField(max_length=255, unique=True, db_column="VP Codice")

    # Core configuration characteristics
    variant = models.CharField(max_length=255, null=True, blank=True, db_column="Variante")
    version = models.CharField(max_length=255, null=True, blank=True, db_column="Versão")
    homologation = models.CharField(max_length=255, null=True, blank=True, db_column="Homologação")
    co2 = models.IntegerField(null=True, blank=True, db_column="CO2")
    tare_kg = models.IntegerField(null=True, blank=True, db_column="TARA")
    engine_code = models.CharField(max_length=255, null=True, blank=True, db_column="Motore_V")

    # Commercial codes
    gama = models.CharField(max_length=255, null=True, blank=True, db_column="GAMA")
    modelo = models.CharField(max_length=255, null=True, blank=True, db_column="MODELO")
    cabina = models.CharField(max_length=255, null=True, blank=True, db_column="CABINA")
    motor = models.CharField(max_length=255, null=True, blank=True, db_column="MOTOR")
    gearbox = models.CharField(max_length=255, null=True, blank=True, db_column="CAIXA VEL")
    wheelbase = models.CharField(max_length=255, null=True, blank=True, db_column="WB")
    dee = models.IntegerField(null=True, blank=True, db_column="DEE")
    hi = models.CharField(max_length=255, null=True, blank=True, db_column="HI")

    # Color
    color_code_numeric = models.IntegerField(null=True, blank=True, db_column="Colore_Codice (Numerico)")
    color_desc = models.CharField(max_length=255, null=True, blank=True, db_column="Colore_Descrizione Estesa")

    notas_vp = models.TextField(null=True, blank=True, db_column="NOTAS_VP")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "vp"
        ordering = ["vp_code"]
        indexes = [
            models.Index(fields=["vp_code"]),
            models.Index(fields=["modelo", "version"]),
        ]

    def __str__(self):
        return self.vp_code


# -------------------------
# Vehicle: physical unit
# -------------------------
class Vehicle(models.Model):

    van = models.IntegerField(primary_key=True,unique=True, db_column="VAN")

    vin = models.CharField(
        max_length=17, null=True, blank=True, db_column="VIN",
        validators=[VIN_REGEX]
    )

    plate = models.CharField(
        max_length=20, null=True, blank=True, db_column="MATRICULA",
        validators=[PLATE_REGEX]
    )
    registration_date = models.DateField(null=True, blank=True, db_column="DATA_MATRICULA")

    lot = models.IntegerField(null=True, blank=True, db_column="LOT")
    country = models.CharField(max_length=255, null=True, blank=True, db_column="Country")
    production_year = models.DateField(null=True, blank=True, db_column="ANO_PROD")

    has_service_campaign = models.BooleanField(default=False, null=True, blank=True, db_column="CAMPANHA_SERVICE")
    service_campaign_date = models.DateField(null=True, blank=True, db_column="CAMPANHA_SERVICE_DATA")
    service_campaign_due = models.DateField(null=True, blank=True, db_column="CAMPANHA_SERVICE_PREV")

    vp = models.ForeignKey(
        VP,
        on_delete=models.PROTECT,
        related_name="vehicles",
        db_column="VP_FK",
        null=False, blank=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "vehicle"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["van"]),
            models.Index(fields=["vin"]),
            models.Index(fields=["plate"]),
            models.Index(fields=["vp"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["vin"], name="uniq_vehicle_vin_nn", condition=models.Q(vin__isnull=False)),
            models.UniqueConstraint(fields=["plate"], name="uniq_vehicle_plate_nn", condition=models.Q(plate__isnull=False)),
        ]

    def __str__(self):
        return f"VAN {self.van} @ {self.vp.vp_code}"

class InternalTransport(models.Model):
    id = models.BigAutoField(primary_key=True)

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="internal_transports",
        db_column="VAN",
        null=True, blank=True,
        help_text="Vehicle (by VAN) used for this internal transport."
    )

    origin = models.CharField(max_length=255, null=True, blank=True, db_column="ORIGEM")
    destination = models.CharField(max_length=255, null=True, blank=True, db_column="DESTINO")

    request_date = models.DateField(null=True, blank=True, db_column="DATA PEDIDO")
    transport_date = models.DateField(null=True, blank=True, db_column="DATA TRANSPORTE")

    notes = models.TextField(null=True, blank=True, db_column="NOTAS")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "internal_transport"
        ordering = ["-request_date"]
        indexes = [
            models.Index(fields=["vehicle", "transport_date"]),
            models.Index(fields=["origin"]),
            models.Index(fields=["destination"]),
        ]

    def __str__(self):
        return f"Transport {self.id}: {self.origin} → {self.destination}"

class OCFStock(models.Model):
    id = models.BigAutoField(primary_key=True)

    vehicle = models.OneToOneField(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="ocf_entry",
        db_column="VAN",
        help_text="The vehicle tracked in OCF stock."
    )

    # --- Sales assignment ---
    has_client = models.BooleanField(default=False, db_column="OCF", help_text="True if vehicle assigned to a client")
    client_assigned_date = models.DateField(null=True, blank=True, db_column="OCF_DATA")
    channel = models.CharField(max_length=255, null=True, blank=True, db_column="CANAL")  # direct / dealer / stock
    distributor = models.CharField(max_length=255, null=True, blank=True, db_column="DISTRIBUIDOR")
    salesperson = models.ForeignKey(
        "Salesperson",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="ocf_sales",
        db_column="VENDEDOR"
    )

    # --- Order details ---
    order_week = models.IntegerField(null=True, blank=True, db_column="SEMANA", help_text="Week number of order")
    order_date = models.DateField(null=True, blank=True, db_column="DATA")
    order_number = models.IntegerField(null=True, blank=True, db_column="NUMERO LATERAL")
    client_name = models.CharField(max_length=255, null=True, blank=True, db_column="CLIENTE")
    client_final = models.CharField(max_length=255, null=True, blank=True, db_column="CLIENTE3")

    # --- Workflow flags ---
    sold = models.BooleanField(default=False, db_column="VENDIDO")
    produced = models.BooleanField(default=False, db_column="PRODUZIDO")
    buyback = models.BooleanField(default=False, db_column="BB")
    extended_warranty = models.BooleanField(default=False, db_column="EW")
    extended_warranty_date = models.DateField(null=True, blank=True, db_column="EW_DATA")
    maintenance_contract = models.BooleanField(default=False, db_column="CMR")
    maintenance_contract_date = models.DateField(null=True, blank=True, db_column="CMR_DATA")

    # --- Logistics ---
    delivery_date = models.DateField(null=True, blank=True, db_column="DATA ENTREGA")
    expected_delivery = models.CharField(max_length=255, null=True, blank=True, db_column="ENTREGA_PREVISTA")
    reservation_info = models.CharField(max_length=255, null=True, blank=True, db_column="RESERVA")
    reservation_notes = models.TextField(null=True, blank=True, db_column="RESERVA_NOTAS")
    reservation_date = models.DateField(null=True, blank=True, db_column="DATA RESERVA")
    location = models.CharField(max_length=255, null=True, blank=True, db_column="LOCALIZAÇÃO")
    location_date = models.DateField(null=True, blank=True, db_column="LOCAL_DATA")

    # --- PDI / warranty workflow ---
    warranty_start = models.DateField(null=True, blank=True, db_column="WSD")
    pre_pdi_date = models.DateField(null=True, blank=True, db_column="DATA_PRE_PDI")
    pdi_request_date = models.DateField(null=True, blank=True, db_column="DATA_PDI_PEDIDO")
    pdi_completed_date = models.DateField(null=True, blank=True, db_column="DATA_PDI_OK")
    pdi_notes = models.TextField(null=True, blank=True, db_column="NOTAS_PDI")
    pdi_workshop = models.CharField(max_length=255, null=True, blank=True, db_column="OFICINA_PDI")

    # --- Campaigns ---
    has_service_campaign = models.BooleanField(default=False, db_column="CAMPANHA_SERVICE")
    service_campaign_date = models.DateField(null=True, blank=True, db_column="CAMPANHA_SERVICE_DATA")
    service_campaign_due = models.DateField(null=True, blank=True, db_column="CAMPANHA_SERVICE_PREV")

    # --- Misc ---
    notes = models.TextField(null=True, blank=True, db_column="NOTAS")
    stock_notes = models.TextField(null=True, blank=True, db_column="Notas_STOCK")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ocf_stock"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["has_client"]),
            models.Index(fields=["sold"]),
            models.Index(fields=["produced"]),
            models.Index(fields=["delivery_date"]),
            models.Index(fields=["salesperson"]),
        ]

    def __str__(self):
        return f"OCF {self.vehicle.van} ({'Sold' if self.sold else 'Stock'})"
