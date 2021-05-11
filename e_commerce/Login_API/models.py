from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy

# To automatically create one to one objects
from django.db.models.signals import post_save
from django.dispatch import receiver


class MyUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set.')

        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff permission')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser permission')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique = True, null = False)

    is_staff = models.BooleanField(
        ugettext_lazy('Staff Status'),
        default = False,
        help_text = ugettext_lazy('Decides if the user is authorized to log in')
    )

    is_active = models.BooleanField(
        ugettext_lazy('Active'),
        default = True,
        help_text = ugettext_lazy('Decides if the user is active')
    )

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'profile')
    username = models.CharField(max_length = 255, blank = True)
    full_name = models.CharField(max_length = 255, blank = True)
    address = models.TextField(max_length = 300, blank = True)
    city = models.CharField(max_length = 86, blank = True)
    zipcode = models.CharField(max_length = 6, blank = True)
    country = models.CharField(max_length = 60, blank = True)
    phone = models.CharField(max_length = 10, blank = True)
    date_joined = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.username + "'s Profile"

    def is_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]

        for field in fields_names:
            value = getattr(self, field)
            if value is None or value == '':
                return False

        return True

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
