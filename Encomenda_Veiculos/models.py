# models.py
from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

PT_NIF_REGEX = RegexValidator(regex=r"^\d{9}$", message=_("NIF must be 9 digits."))
PT_POSTAL_REGEX = RegexValidator(regex=r"^\d{4}-\d{3}$", message=_("Postal code must be NNNN-NNN."))
PHONE_REGEX = RegexValidator(regex=r"^[0-9+\-\s().]{7,20}$", message=_("Invalid phone number format."))

VIN_REGEX = RegexValidator(
    regex=r"^[A-HJ-NPR-Z0-9]{11,17}$",
    message=_("VIN must be 11–17 characters (alphanumeric, excluding I/O/Q).")
)
PLATE_REGEX = RegexValidator(
    regex=r"^[A-Z0-9\- ]{5,15}$",
    message=_("License plate should be 5–15 chars (letters/digits/hyphens/spaces).")
)

class Salesperson(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="salesperson_profile",
        verbose_name=_("User"),
        help_text=_("User account for this salesperson.")
    )

    distributor = models.CharField(max_length=255, null=True, blank=True, db_column="DISTRIBUIDOR", verbose_name=_("Distributor"))
    active = models.BooleanField(default=True, db_column="ATIVO", verbose_name=_("Active"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        db_table = "salesperson"
        verbose_name = _("Salesperson")
        verbose_name_plural = _("Salespeople")
        ordering = ["user__username"]
        indexes = [
            models.Index(fields=["distributor"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=20, db_column="Cliente_Codice", verbose_name=_("Code"))
    name = models.CharField(max_length=200, db_column="Cliente_Nome", verbose_name=_("Name"))

    nif = models.CharField(
        max_length=9, null=True, blank=True, db_column="NIF",
        validators=[PT_NIF_REGEX],
        verbose_name=_("NIF"),
        help_text=_("Portuguese taxpayer number (9 digits).")
    )
    address = models.CharField(max_length=255, null=True, blank=True, db_column="Morada", verbose_name=_("Address"))
    postal_code = models.CharField(
        max_length=8, null=True, blank=True, db_column="Cod_Postal",
        validators=[PT_POSTAL_REGEX],
        verbose_name=_("Postal Code")
    )
    city = models.CharField(max_length=120, null=True, blank=True, db_column="Localidade", verbose_name=_("City"))

    phone = models.CharField(
        max_length=30, null=True, blank=True, db_column="Tel_geral",
        validators=[PHONE_REGEX],
        verbose_name=_("Phone")
    )
    email = models.EmailField(null=True, blank=True, db_column="Mail_geral", verbose_name=_("Email"))

    distributor = models.CharField(max_length=120, null=True, blank=True, db_column="Distribuidor", verbose_name=_("Distributor"))
    seller = models.CharField(max_length=120, null=True, blank=True, db_column="Vendedor", verbose_name=_("Seller"))

    pending_review = models.BooleanField(default=False, db_column="PENDING_REVIEW", verbose_name=_("Pending Review"))

    updated_at = models.DateTimeField(null=True, blank=True, db_column="Ultimo_Atualizar", verbose_name=_("Updated At"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        db_table = "client"
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
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
        verbose_name=_("Client"),
        help_text=_("Owning client.")
    )

    name = models.CharField(max_length=200, verbose_name=_("Name"), help_text=_("Contact person name."))
    job_title = models.CharField(max_length=120, null=True, blank=True, verbose_name=_("Job Title"))
    email = models.EmailField(null=True, blank=True, verbose_name=_("Email"))
    phone = models.CharField(
        max_length=30, null=True, blank=True,
        validators=[PHONE_REGEX],
        verbose_name=_("Phone")
    )

    is_primary = models.BooleanField(default=False, verbose_name=_("Is Primary"), help_text=_("Marks this as the primary contact for the client."))
    notes = models.TextField(null=True, blank=True, verbose_name=_("Notes"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        db_table = "client_contact"
        verbose_name = _("Client Contact")
        verbose_name_plural = _("Client Contacts")
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
    vp_code = models.CharField(max_length=255, unique=True, db_column="VP Codice", verbose_name=_("VP Code"))

    variant = models.CharField(max_length=255, null=True, blank=True, db_column="Variante", verbose_name=_("Variant"))
    version = models.CharField(max_length=255, null=True, blank=True, db_column="Versão", verbose_name=_("Version"))
    homologation = models.CharField(max_length=255, null=True, blank=True, db_column="Homologação", verbose_name=_("Homologation"))
    co2 = models.IntegerField(null=True, blank=True, db_column="CO2", verbose_name=_("CO2"))
    tare_kg = models.IntegerField(null=True, blank=True, db_column="TARA", verbose_name=_("Tare (kg)"))
    engine_code = models.CharField(max_length=255, null=True, blank=True, db_column="Motore_V", verbose_name=_("Engine Code"))

    gama = models.CharField(max_length=255, null=True, blank=True, db_column="GAMA", verbose_name=_("Gama"))
    modelo = models.CharField(max_length=255, null=True, blank=True, db_column="MODELO", verbose_name=_("Modelo"))
    cabina = models.CharField(max_length=255, null=True, blank=True, db_column="CABINA", verbose_name=_("Cabina"))
    motor = models.CharField(max_length=255, null=True, blank=True, db_column="MOTOR", verbose_name=_("Motor"))
    gearbox = models.CharField(max_length=255, null=True, blank=True, db_column="CAIXA VEL", verbose_name=_("Gearbox"))
    wheelbase = models.CharField(max_length=255, null=True, blank=True, db_column="WB", verbose_name=_("Wheelbase"))
    dee = models.IntegerField(null=True, blank=True, db_column="DEE", verbose_name=_("DEE"))
    hi = models.CharField(max_length=255, null=True, blank=True, db_column="HI", verbose_name=_("HI"))

    color_code_numeric = models.IntegerField(null=True, blank=True, db_column="Colore_Codice (Numerico)", verbose_name=_("Color Code (Numeric)"))
    color_desc = models.CharField(max_length=255, null=True, blank=True, db_column="Colore_Descrizione Estesa", verbose_name=_("Color Description"))

    notas_vp = models.TextField(null=True, blank=True, db_column="NOTAS_VP", verbose_name=_("VP Notes"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(default=timezone.now, verbose_name=_("Updated At"))

    class Meta:
        db_table = "vp"
        verbose_name = _("VP")
        verbose_name_plural = _("VPs")
        ordering = ["vp_code"]
        indexes = [
            models.Index(fields=["vp_code"]),
            models.Index(fields=["modelo", "version"]),
        ]

    def __str__(self):
        return self.vp_code


class Vehicle(models.Model):
    van = models.IntegerField(primary_key=True, unique=True, db_column="VAN", verbose_name=_("VAN"))

    vin = models.CharField(
        max_length=17, null=True, blank=True, db_column="VIN",
        validators=[VIN_REGEX],
        verbose_name=_("VIN")
    )

    plate = models.CharField(
        max_length=20, null=True, blank=True, db_column="MATRICULA",
        validators=[PLATE_REGEX],
        verbose_name=_("License Plate")
    )
    registration_date = models.DateField(null=True, blank=True, db_column="DATA_MATRICULA", verbose_name=_("Registration Date"))

    lot = models.IntegerField(null=True, blank=True, db_column="LOT", verbose_name=_("Lot"))
    country = models.CharField(max_length=255, null=True, blank=True, db_column="Country", verbose_name=_("Country"))
    production_year = models.DateField(null=True, blank=True, db_column="ANO_PROD", verbose_name=_("Production Year"))

    has_service_campaign = models.BooleanField(default=False, null=True, blank=True, db_column="CAMPANHA_SERVICE", verbose_name=_("Has Service Campaign"))
    service_campaign_date = models.DateField(null=True, blank=True, db_column="CAMPANHA_SERVICE_DATA", verbose_name=_("Service Campaign Date"))
    service_campaign_due = models.DateField(null=True, blank=True, db_column="CAMPANHA_SERVICE_PREV", verbose_name=_("Service Campaign Due"))

    vp = models.ForeignKey(
        VP,
        on_delete=models.PROTECT,
        related_name="vehicles",
        db_column="VP_FK",
        null=False, blank=False,
        verbose_name=_("VP")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(default=timezone.now, verbose_name=_("Updated At"))

    class Meta:
        db_table = "vehicle"
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")
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
        verbose_name=_("Vehicle"),
        help_text=_("Vehicle (by VAN) used for this internal transport.")
    )

    origin = models.CharField(max_length=255, null=True, blank=True, db_column="ORIGEM", verbose_name=_("Origin"))
    destination = models.CharField(max_length=255, null=True, blank=True, db_column="DESTINO", verbose_name=_("Destination"))

    request_date = models.DateField(null=True, blank=True, db_column="DATA PEDIDO", verbose_name=_("Request Date"))
    transport_date = models.DateField(null=True, blank=True, db_column="DATA TRANSPORTE", verbose_name=_("Transport Date"))

    notes = models.TextField(null=True, blank=True, db_column="NOTAS", verbose_name=_("Notes"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        db_table = "internal_transport"
        verbose_name = _("Internal Transport")
        verbose_name_plural = _("Internal Transports")
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
        verbose_name=_("Vehicle"),
        help_text=_("The vehicle tracked in OCF stock.")
    )

    has_client = models.BooleanField(default=False, db_column="OCF", verbose_name=_("Has Client"), help_text=_("True if vehicle assigned to a client"))
    client_assigned_date = models.DateField(null=True, blank=True, db_column="OCF_DATA", verbose_name=_("Client Assigned Date"))
    channel = models.CharField(max_length=255, null=True, blank=True, db_column="CANAL", verbose_name=_("Channel"))
    distributor = models.CharField(max_length=255, null=True, blank=True, db_column="DISTRIBUIDOR", verbose_name=_("Distributor"))
    salesperson = models.ForeignKey(
        "Salesperson",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="ocf_sales",
        db_column="VENDEDOR",
        verbose_name=_("Salesperson")
    )

    order_week = models.IntegerField(null=True, blank=True, db_column="SEMANA", verbose_name=_("Order Week"), help_text=_("Week number of order"))
    order_date = models.DateField(null=True, blank=True, db_column="DATA", verbose_name=_("Order Date"))
    order_number = models.IntegerField(null=True, blank=True, db_column="NUMERO LATERAL", verbose_name=_("Order Number"))
    client_name = models.CharField(max_length=255, null=True, blank=True, db_column="CLIENTE", verbose_name=_("Client Name"))
    client_final = models.CharField(max_length=255, null=True, blank=True, db_column="CLIENTE3", verbose_name=_("Final Client"))

    sold = models.BooleanField(default=False, db_column="VENDIDO", verbose_name=_("Sold"))
    produced = models.BooleanField(default=False, db_column="PRODUZIDO", verbose_name=_("Produced"))
    buyback = models.BooleanField(default=False, db_column="BB", verbose_name=_("Buyback"))
    extended_warranty = models.BooleanField(default=False, db_column="EW", verbose_name=_("Extended Warranty"))
    extended_warranty_date = models.DateField(null=True, blank=True, db_column="EW_DATA", verbose_name=_("Extended Warranty Date"))
    maintenance_contract = models.BooleanField(default=False, db_column="CMR", verbose_name=_("Maintenance Contract"))
    maintenance_contract_date = models.DateField(null=True, blank=True, db_column="CMR_DATA", verbose_name=_("Maintenance Contract Date"))

    delivery_date = models.DateField(null=True, blank=True, db_column="DATA ENTREGA", verbose_name=_("Delivery Date"))
    expected_delivery = models.CharField(max_length=255, null=True, blank=True, db_column="ENTREGA_PREVISTA", verbose_name=_("Expected Delivery"))
    reservation_info = models.CharField(max_length=255, null=True, blank=True, db_column="RESERVA", verbose_name=_("Reservation Info"))
    reservation_notes = models.TextField(null=True, blank=True, db_column="RESERVA_NOTAS", verbose_name=_("Reservation Notes"))
    reservation_date = models.DateField(null=True, blank=True, db_column="DATA RESERVA", verbose_name=_("Reservation Date"))
    location = models.CharField(max_length=255, null=True, blank=True, db_column="LOCALIZAÇÃO", verbose_name=_("Location"))
    location_date = models.DateField(null=True, blank=True, db_column="LOCAL_DATA", verbose_name=_("Location Date"))

    warranty_start = models.DateField(null=True, blank=True, db_column="WSD", verbose_name=_("Warranty Start"))
    pre_pdi_date = models.DateField(null=True, blank=True, db_column="DATA_PRE_PDI", verbose_name=_("Pre-PDI Date"))
    pdi_request_date = models.DateField(null=True, blank=True, db_column="DATA_PDI_PEDIDO", verbose_name=_("PDI Request Date"))
    pdi_completed_date = models.DateField(null=True, blank=True, db_column="DATA_PDI_OK", verbose_name=_("PDI Completed Date"))
    pdi_notes = models.TextField(null=True, blank=True, db_column="NOTAS_PDI", verbose_name=_("PDI Notes"))
    pdi_workshop = models.CharField(max_length=255, null=True, blank=True, db_column="OFICINA_PDI", verbose_name=_("PDI Workshop"))

    has_service_campaign = models.BooleanField(default=False, db_column="CAMPANHA_SERVICE", verbose_name=_("Has Service Campaign"))
    service_campaign_date = models.DateField(null=True, blank=True, db_column="CAMPANHA_SERVICE_DATA", verbose_name=_("Service Campaign Date"))
    service_campaign_due = models.DateField(null=True, blank=True, db_column="CAMPANHA_SERVICE_PREV", verbose_name=_("Service Campaign Due"))

    notes = models.TextField(null=True, blank=True, db_column="NOTAS", verbose_name=_("Notes"))
    stock_notes = models.TextField(null=True, blank=True, db_column="Notas_STOCK", verbose_name=_("Stock Notes"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        db_table = "ocf_stock"
        verbose_name = _("OCF Stock")
        verbose_name_plural = _("OCF Stocks")
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
