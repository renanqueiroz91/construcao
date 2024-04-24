from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings

class MyUserManager(BaseUserManager):
    def create_user(self, nome, tipo, sobrenome, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            nome=nome,
            sobrenome=sobrenome,
            tipo=tipo,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, tipo, nome, sobrenome, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            password=password,
            nome=nome,
            sobrenome=sobrenome,
            email=email,
            tipo=tipo,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    user_type = (
        ('','------'),
        ('admin','admin'),
        ('user','user'),
    )


    nome = models.CharField(max_length=255, default='')
    sobrenome = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.CharField(max_length=15, choices=user_type, default='user')
    email = models.EmailField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)


    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'sobrenome','tipo']

    def __str__(self):
        return self.nome

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def get_user_type(self):
            if self.is_admin:
                return 'admin'
            else:
                return 'user'

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"