from jwt import PyJWT
from typing import Optional
from datetime import (
    datetime,
    timedelta
)

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

jwt_manager = PyJWT()
TOKEN_LIFETIME_DAYS = 60


class UserManager(BaseUserManager):

    def _lowercase_domain(self, email_address):
        return self.normalize_email(email_address)

    def create_user(self, username: str, email: str, password: Optional[str] = None) -> 'User':
        if username is None:
            raise TypeError('Username is required.')
        if email is None:
            raise TypeError('Email is required.')

        user = self.model(username=username, email=self._lowercase_domain(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username: str, email: str, password: str) -> 'User':
        def grant_super_permissions(would_be_superuser: 'User') -> 'User':
            would_be_superuser.is_superuser = True
            would_be_superuser.is_staff = True
            return would_be_superuser

        if password is None:
            raise TypeError('Password is required for admin user')
        user = self.create_user(username, email, password)
        grant_super_permissions(user)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt(self) -> str:
        expires_at = datetime.now() + timedelta(days=TOKEN_LIFETIME_DAYS)
        token = jwt_manager.encode(
            algorithm='HS256',
            payload={
                'id': self.pk,
                'exp': int(expires_at.strftime('%s'))
            },
            key=settings.SECRET_KEY
        )
        return token

    @property
    def token(self) -> str:
        return self._generate_jwt()
