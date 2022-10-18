from django.db import models
from django.contrib.auth.models import AbstractBaseUser,\
    PermissionsMixin, BaseUserManager
from django.core import validators


class UserQuerySet(models.QuerySet):
    pass


class UserManager(BaseUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self.db)

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given phone and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    # Username
    email = models.EmailField(max_length=70, unique=True)

    # Validators
    phone_regex = validators.RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                            message="Phone number must be entered in the format:"
                                                    " '+999999999'. Up to 15 digits allowed.")
    # User Fields
    first_name = models.CharField('First Name', max_length=40, blank=True)
    last_name = models.CharField('Last Name', max_length=40, blank=True)
    middle_name = models.CharField('Middle Name', max_length=40, blank=True, null=True)
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)

    is_superuser = models.BooleanField('Is a superuser', default=False)
    is_admin = models.BooleanField('Is a admin', default=False)
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return f'{self.id} - {self.first_name} {self.last_name}'

