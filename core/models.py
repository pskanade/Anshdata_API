from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, is_producer=False, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email address must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, is_producer=is_producer, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, is_producer=False, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, is_producer, **extra_fields)

    def create_superuser(self, username, email, password, is_producer=True, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, is_producer, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(_("Email address"),
                              blank=False,
                              unique=True,
                              db_index=True)
    last_updated = models.DateTimeField(_("Info updated on"),
                                        blank=True,
                                        editable=False,
                                        help_text="This field reflects the date and time"
                                                  " when the user information was last updated")
    is_producer = models.BooleanField(_("is producer"),
                                      default=False,
                                      blank=True,
                                      help_text="This is to simply find if the user is going"
                                                " to create courses or opting for the courses")
    last_login = models.DateTimeField(_("Last login time"),
                                      blank=True,
                                      editable=False,
                                      help_text="Stores the last login time and date of the user")
    objects = UserManager()


class Producer(models.Model):
    user = models.OneToOneField(User,
                                primary_key=True,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name="General User Info",
                                help_text="Refers to the generic information that platform has collected on signup")
    company_name = models.CharField(_("Company Name"),
                                    max_length=255,
                                    blank=True,
                                    help_text="Collects ")


class Consumer(models.Model):
    user = models.OneToOneField(User,
                                primary_key=True,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name="General User Info",
                                help_text="Refers to the generic information that platform has collected on signup")
    date_of_birth = models.DateField(_("Date of Birth"),
                                     blank=True,
                                     help_text="Field describes the date of birth which will "
                                               "help us find the age of the user")
