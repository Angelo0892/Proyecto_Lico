from django.db import migrations, models

def crear_permisos_predeterminados(apps, schema_editor):
    Permiso = apps.get_model('dashboard', 'Permiso')

    permisos = [
        ("modulo_dashboard", "Acceso al dashboard"),
        ("modulo_usuarios", "Gestión de usuarios"),
        ("modulo_categorias", "Gestión de categorías"),
        ("modulo_facturacion", "Facturación y ventas"),
        ("modulo_proveedores", "Gestión de proveedores"),
        ("modulo_productos", "Gestión de productos"),
        ("modulo_importaciones", "Gestión de importaciones"),
        ("modulo_reportes", "Acceso a reportes"),
    ]

    for nombre, descripcion in permisos:
        Permiso.objects.get_or_create(
            nombre=nombre,
            defaults={"descripcion": descripcion}
        )

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_importacion_stock_ingresado'),
    ]

    operations = [
        migrations.AddField(
            model_name='rol',
            name='permisos',
            field=models.ManyToManyField(blank=True, to='dashboard.Permiso'),
        ),
        migrations.RunPython(crear_permisos_predeterminados),
    ]