import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from cliente.models import Cliente, Beneficiario


class Command(BaseCommand):
    help = 'Importar beneficiarios desde CSV'

    def handle(self, *args, **kwargs):

        ruta_csv = os.path.join(
            settings.BASE_DIR,
            'importaciones',
            'management',
            'commands',
            'beneficiarios.csv'
        )

        with open(ruta_csv, newline='', encoding='utf-8-sig') as archivo:
            reader = csv.DictReader(archivo)

            # 🔴 LIMPIA encabezados
            reader.fieldnames = [h.strip().lower() for h in reader.fieldnames]

            for fila in reader:
                # 🔴 LIMPIA claves por fila
                fila = {k.strip().lower(): v for k, v in fila.items()}

                poliza = fila.get('poliza')

                if not poliza:
                    self.stdout.write(
                        self.style.WARNING('⚠ Fila sin póliza, se omite')
                    )
                    continue

                try:
                    cliente = Cliente.objects.get(poliza=poliza.strip())
                except Cliente.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'❌ Cliente no encontrado: {poliza}')
                    )
                    continue

                Beneficiario.objects.create(
                    nombre_contratante=cliente,
                    nombre_beneficiario=fila.get('nombre_beneficiario'),
                    fecha_nacimiento_beneficiario=fila.get('fecha_nacimiento_beneficiario') or None,
                    parentesco=fila.get('parentesco'),
                    estatus_beneficiario=fila.get('estatus_beneficiario', 'beneficiario')
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'✔ Beneficiario {fila.get("nombre_beneficiario")} agregado a póliza {poliza}'
                    )
                )
