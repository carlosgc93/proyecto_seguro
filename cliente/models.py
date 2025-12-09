from django.db import models

# ======================
# MODELO CLIENTE
# ======================
class  Cliente(models.Model):
    # Definir las opciones como tuplas
    OPCIONES_ESTATUS = [
        ('en_vigor', 'En Vigor'),
        ('anulada', 'Anulada'),
    ]
    OPCIONES_DEDUCE = [
        ('si', 'Si'),
        ('no', 'No'),
    ]
    OPCIONES_PERIODO_PAGO = [
        ('mensual', 'Mensual'),
        ('trimestral', 'Trimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
    ]

    OPCIONES_MODO_PAGO = [
        ('agente', 'Agente'),
        ('directo', 'Directo'),
        ('tdc', 'TDC'),
        ('tdd', 'TDD'),
    ]

    OPCIONES_MONEDA = [
        ('peso', 'Peso'),
        ('udi', 'UDI'),
        ('usd', 'USD'),
    ]

    OPCIONES_PRODUCTO = [
        ('alfa_medical_flex', 'Alfa Medical Flex'),
        ('integro', 'Integro'),
        ('pleno', 'Pleno'),
        ('practico', 'Practico'),
        ('imagina_ser_55', 'Imagina Ser 55'),
        ('imagina_ser_60', 'Imagina Ser 60'),
        ('imagina_ser_65', 'Imagina Ser 65'),
        ('imagina_ser_70', 'Imagina Ser 70'),
        ('legado', 'Legado'),
        ('nuevo_plenitud', 'Nuevo Plenitud'),
        ('objetivo_vida', 'Objetivo Vida'),
        ('orvi_6', 'ORVI 6'),
        ('orvi_10', 'ORVI 10'),
        ('orvi_15', 'ORVI 15'),
        ('orvi_20', 'ORVI 20'),
        ('realiza_creciente','Realiza Creciente'),
        ('segubeca', 'Segubeca'),
        ('tempo_vida', 'Tempo Vida'),
        ('temporal', 'Temporal'),
        ('vida_joven', 'Vida Joven'),
        ('vida_mil', 'Vida Mil'),
        ('vida_mujer', 'Vida Mujer'),
        ('vida_plena', 'Vida Plena'),
        ('visualiza', 'Visualiza'),
    ]
    poliza = models.CharField(max_length=50, verbose_name="No. Póliza")
    nombre_contratante = models.CharField(max_length=250)
    sobrenombre = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(
        verbose_name="Fecha de Nacimiento",
        help_text="F: DD/MM/AAAA",blank=True, null=True)
    asegurado_principal = models.CharField(max_length=250,blank=True, null=True)
    fecha_nacimiento_asegurado = models.DateField(blank=True, null=True, verbose_name="F. Nac. Asegurado")
    #producto = models.CharField(max_length=100)
    producto = models.CharField(
        max_length=100,
        choices=OPCIONES_PRODUCTO
    )

    estatus_cliente= models.CharField(
        max_length=20,
        choices=OPCIONES_ESTATUS,
        default='en_vigor')  # valor por defecto

    deduce = models.CharField(
        max_length=20,
        choices=OPCIONES_DEDUCE,
        blank=True,
        null=True)

    rfc = models.CharField(max_length=13, blank=True, null=True)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    fecha_emision = models.DateField(blank=True, null=True)

    moneda = models.CharField(
        max_length=20,
        choices=OPCIONES_MONEDA,
        blank=True,
        null=True
    )

    modo_pago = models.CharField(
        verbose_name="Modo de Pago",
        max_length=50,
        choices=OPCIONES_MODO_PAGO,
        blank=True,
        null=True
    )

    banco = models.CharField(max_length=50, blank=True, null=True)
    periodo_pago = models.CharField(
        max_length=50,
        choices=OPCIONES_PERIODO_PAGO,
        blank=True,
        null=True
    )
    dia_cobro = models.PositiveIntegerField(blank=True, null=True)
    rechazo = models.BooleanField(default=False, blank=True, null=True)
    intentos = models.IntegerField(default=0, blank=True, null=True)
    amparado = models.CharField(max_length=50, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_contratante} - Póliza {self.poliza}"


# ======================
# MODELO BENEFICIARIO
# ======================
class Beneficiario(models.Model):
    PARENTESCO_CHOICES = [
        ('madre', 'Madre'),
        ('padre', 'Padre'),
        ('hijo', 'Hijo'),
        ('hija', 'Hija'),
        ('hermano', 'Hermano'),
        ('hermana', 'Hermana'),
        ('esposo', 'Esposo'),
        ('esposa', 'Esposa'),
        ('nieto', 'Nieto'),
        ('nieta', 'Nieta'),
        ('sobrino', 'Sobrino'),
        ('sobrina', 'Sobrina'),
        ('primo', 'Primo'),
        ('prima', 'Prima'),
        ('tutor', 'Tutor'),
        ('tutora', 'Tutora'),
        ('pareja', 'Pareja'),
        ('abuelo', 'Abuelo'),
        ('abuela', 'Abuela'),
        ('ninguno', 'Ninguno'),
    ]

    ESTATUS_CHOICES = [
        ('asegurado', 'Asegurado'),
        ('beneficiario', 'Beneficiario'),
    ]

    nombre_contratante = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='beneficiarios'
    )
    nombre_beneficiario = models.CharField(max_length=200)
    fecha_nacimiento_beneficiario = models.DateField(blank=True, null=True)

    parentesco = models.CharField(
        max_length=25,
        choices=PARENTESCO_CHOICES,
        blank=True,
        null=True,
    )

    estatus_beneficiario = models.CharField(
        max_length=25,
        choices=ESTATUS_CHOICES,
        blank=True,
        null=True,
        default='beneficiario',
    )

    def __str__(self):
        parentesco = self.parentesco if self.parentesco else "Sin parentesco"
        return f"{self.nombre_beneficiario} ({parentesco})"




