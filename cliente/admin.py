from django.contrib import admin
from .models import Cliente, Beneficiario
from django.utils.html import format_html, format_html_join


# ======================
# Filtro para los meses
# ======================

class MesNacimientoFilter(admin.SimpleListFilter):
    title = 'Mes de Nacimiento'
    parameter_name = 'mes_nacimiento'

    def lookups(self, request, model_admin):
        # Lista de meses (número, nombre)
        return [
            (1, 'Enero'),
            (2, 'Febrero'),
            (3, 'Marzo'),
            (4, 'Abril'),
            (5, 'Mayo'),
            (6, 'Junio'),
            (7, 'Julio'),
            (8, 'Agosto'),
            (9, 'Septiembre'),
            (10, 'Octubre'),
            (11, 'Noviembre'),
            (12, 'Diciembre'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(fecha_nacimiento__month=self.value())
        return queryset
#
# ======================
# INLINE: Beneficiarios dentro del Cliente
# ======================
class BeneficiarioInline(admin.TabularInline):
    model = Beneficiario
    extra = 0  # Muestra un formulario vacío adicional
    fields = ('nombre_beneficiario', 'parentesco','estatus_beneficiario','fecha_nacimiento_beneficiario')




# ======================
# ADMIN CLIENTE
# ======================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('poliza', 'nombre_contratante', 'producto', 'estatus_cliente', 'fecha_vencimiento')
    search_fields = ('poliza', 'nombre_contratante', 'rfc', 'correo')
    list_filter = (MesNacimientoFilter,'estatus_cliente', 'producto', 'banco', 'modo_pago')
    ordering = ('poliza',)
    inlines = [BeneficiarioInline]  # Muestra los beneficiarios dentro del cliente
    fieldsets = (
        ('Información General', {
            'fields': ('poliza', 'nombre_contratante', 'sobrenombre', 'fecha_nacimiento', 'producto', 'estatus_cliente')
        }),
        ('Detalles del Contrato', {
            'fields': ('deduce', 'rfc', 'correo', 'fecha_emision', 'fecha_vencimiento')
        }),
        ('Pago y Cobranza', {
            'fields': ('moneda', 'modo_pago', 'banco', 'periodo_pago', 'dia_cobro', 'rechazo', 'intentos', 'amparado')
        }),
    )
def mostrar_beneficiarios(self, obj):
    beneficiarios = obj.beneficiarios.all()
    if not beneficiarios.exists():
        add_url = f"/admin/seguros/beneficiario/add/?cliente={obj.id_cliente}"
        return format_html(f"— No hay beneficiarios — <a href='{add_url}' class='button'>Agregar uno</a>")

    html = format_html_join(
        '\n',
        "<li><a href='/admin/seguros/beneficiario/{}/change/'><strong>{}</strong></a> ({}) — <span style='color: #2a9d8f;'>{}</span></li>",
        ((b.id, b.nombre_beneficiario, b.parentesco or 'Sin parentesco', b.estatus or 'Sin estatus') for b in beneficiarios)
    )
    add_url = f"/admin/seguros/beneficiario/add/?cliente={obj.id_cliente}"
    return format_html(f"<ul>{html}</ul><a href='{add_url}' class='button'>➕ Agregar Beneficiario</a>")

# ======================
# ADMIN BENEFICIARIO
# ======================
@admin.register(Beneficiario)
class BeneficiarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_beneficiario', 'parentesco', 'estatus_beneficiario', 'nombre_contratante')
    list_filter = (MesNacimientoFilter,)
    search_fields = ('nombre_beneficiario','nombre_contratante__poliza', 'nombre_contratante__nombre_contratante',)
    ordering = ('id',)
