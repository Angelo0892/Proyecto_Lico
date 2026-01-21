from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, Group
from django.db import models
from django.conf import settings

# =========================
# 1️⃣ Manager personalizado
# =========================
class UsuarioManager(BaseUserManager):

    def create_user(self, correo, nombre_usuario, password=None, **extra_fields):
        if not correo:
            raise ValueError("El usuario debe tener un correo electrónico")
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, nombre_usuario=nombre_usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, nombre_usuario, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correo, nombre_usuario, password, **extra_fields)

# =========================
# 2️⃣ Roles
# =========================
class Roles(models.Model):

    class Meta:
        verbose_name = "Roles"
        verbose_name_plural = "Roles"

    nombre_rol = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_rol

# =========================
# 3️⃣ Permisos de negocio
# =========================
class Permisos(models.Model):
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name='permisos')
    nombre_permiso = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nombre_permiso} - {self.rol.nombre_rol}"

# =========================
# 4️⃣ Usuario personalizado
# =========================
class Usuarios(AbstractBaseUser, PermissionsMixin):
    rol = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_usuario = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=50)
    apellido2 = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=150)
    estado = models.BooleanField(default=True)

    # Campos requeridos por Django
    is_staff = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True)  

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'           # Login con correo
    REQUIRED_FIELDS = ['nombre_usuario']

    def __str__(self):
        return self.nombre_usuario

    # =========================
    # Métodos auxiliares
    # =========================
    def asignar_rol(self, rol):
        """
        Asigna un rol al usuario y sincroniza permisos con el sistema de Django
        """
        self.rol = rol
        self.save()

        # Crear grupo Django con el nombre del rol si no existe
        grupo, created = Group.objects.get_or_create(name=rol.nombre_rol)

        # Agregar permisos de negocio al grupo (opcional: usar content_type genérico)
        for permiso in rol.permisos.all():
            # Crear permiso Django si no existe
            django_perm, created = Permission.objects.get_or_create(
                codename=permiso.nombre_permiso.lower().replace(" ", "_"),
                name=permiso.descripcion,
                content_type_id=1  # Por simplicidad, asigna un content_type real si quieres
            )
            grupo.permissions.add(django_perm)

        # Asignar grupo al usuario
        self.groups.add(grupo)

    def tiene_permiso(self, nombre_permiso):
        """
        Verifica si el usuario tiene un permiso de negocio
        """
        if self.rol:
            return self.rol.permisos.filter(nombre_permiso=nombre_permiso).exists()
        return False