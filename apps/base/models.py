from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.dispatch import receiver  # add this
from django.db.models.signals import post_save  # add this


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone:
            raise ValueError('The given phone must be set')
        self.phone = phone
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        """Create and save a regular User with the given phone and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class CustomUser(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17,
                             unique=True)  # validators should be a list
    city = models.CharField(max_length=50, blank=True, null=True)
    USERNAME_FIELD = 'phone'
    # REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'CustomUser'


class User(models.Model):
    phone = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # pic = models.ImageField(upload_to='user_image', default="avatar.svg")
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    @receiver(post_save, sender=CustomUser)  # add this
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            User.objects.create(phone=instance, first_name=instance.first_name, last_name=instance.last_name)

    @receiver(post_save, sender=CustomUser)  # add this
    def save_user_profile(sender, instance, **kwargs):
        user = instance.user_set.first()
        user.phone = instance
        user.first_name = instance.first_name
        user.last_name = instance.last_name
        user.save()


class BaseAbstractDate(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Variant(BaseAbstractDate):
    duration = models.IntegerField()
    percent = models.IntegerField()

    def __str__(self):
        return str(self.duration)
