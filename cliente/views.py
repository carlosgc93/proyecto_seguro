from django.shortcuts import redirect, get_object_or_404
from cliente.models import Cliente, Beneficiario
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.db.models import Q
from django.urls import reverse_lazy
from .forms import ClienteForm, BeneficiarioForm
from django.contrib.auth.mixins import LoginRequiredMixin


# =====================================================
# =====================VISTAS DE CLIENTES==============
# =====================================================
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "cliente/cliente_list.html"
    paginate_by = 15
    ordering = ['-id']
    login_url = 'usuarios:login'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q")
        mes_nac = self.request.GET.get("mes_nac")
        mes = self.request.GET.get("mes")
        anio = self.request.GET.get("anio")
        producto = self.request.GET.get("producto")

        if q:
            queryset = queryset.filter(
                Q(nombre_contratante__icontains=q) |
                Q(poliza__icontains=q) |
                Q(rfc__icontains=q)
            )

        if mes_nac:
            queryset = queryset.filter(fecha_nacimiento__month=mes_nac)

        if mes:
            queryset = queryset.filter(fecha_emision__month=mes)

        if anio:
            queryset = queryset.filter(fecha_emision__year=anio)

        if producto:
            # Filtrado exacto por la clave del choice
            queryset = queryset.filter(producto=producto)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # años disponibles
        context["años_emision"] = (
            Cliente.objects.exclude(fecha_emision__isnull=True)
            .dates("fecha_emision", "year")
        )

        # PASAR las opciones de producto al template (evita depender de 'form')
        context["productos_choices"] = Cliente._meta.get_field('producto').choices

        return context


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente  # nombre del modelo a usar
    form_class = ClienteForm  # personaliza los campos del modelo desde el forms.py
    template_name = "cliente/cliente_form.html"  # crea este template
    success_url = reverse_lazy("cliente:cliente-list")  # redirige a tu lista
    login_url = 'usuarios:login'


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "cliente/cliente_update_form.html"
    success_url = reverse_lazy("cliente:cliente-list")
    login_url = 'usuarios:login'


class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = "cliente/cliente_detail.html"
    context_object_name = "cliente"
    login_url = 'usuarios:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["beneficiario_form"] = BeneficiarioForm()

        return context


# =====================================================
# =====================VISTAS DE BENEFICIARIO==========
# =====================================================

class BeneficiarioListView(LoginRequiredMixin, ListView):
    model = Beneficiario
    paginate_by = 5  # if pagination is desired
    ordering = ['-id']
    login_url = 'usuarios:login'


def crear_beneficiario(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == "POST":
        form = BeneficiarioForm(request.POST)

        if form.is_valid():
            beneficiario = form.save(commit=False)
            beneficiario.nombre_contratante = cliente
            beneficiario.save()

    return redirect("cliente:cliente_detalle", pk=cliente.id)

def eliminar_beneficiario(request, beneficiario_id):
    beneficiario = get_object_or_404(Beneficiario, id=beneficiario_id)
    cliente_id = beneficiario.nombre_contratante.id

    beneficiario.delete()

    return redirect("cliente:cliente_detalle", pk=cliente_id)