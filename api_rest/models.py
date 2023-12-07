from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo de email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150, default="")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    RACA_CHOICES = (
        ('Branca', 'Branca'),
        ('Preta', 'Preta'),
        ('Amarela', 'Amarela'),
        ('Parda', 'Parda'),
        ('Indígena', 'Indígena'),
    )
    raca = models.CharField(max_length=8, choices=RACA_CHOICES)

    REGIAO_CHOICES = (
        ('Norte', 'Norte'),
        ('Nordeste', 'Nordeste'),
        ('Sul', 'Sul'),
        ('Sudeste', 'Sudeste'),
        ('Centro-Oeste', 'Centro-Oeste'),
    )
    regiao = models.CharField(max_length=35, choices=REGIAO_CHOICES)

    nome_ies = models.CharField(max_length=150, default="")

    modalidade_ensino = models.CharField(max_length=150, default="")

    nome_curso = models.CharField(max_length=150, default="")

    nome_turno_curso = models.CharField(max_length=150, default="")

    sigla_uf_beneficiario = models.CharField(max_length=2, default="")

    municipio_beneficiario = models.CharField(max_length=150, default="")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'password', 'sexo', 'regiao', 'raca', 'nome_ies', 'modalidade_ensino', 'nome_curso', 'nome_turno_curso', 'sigla_uf_beneficiario', 'municipio_beneficiario']


class Resultado_ia(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    resultado = models.CharField(max_length=150)