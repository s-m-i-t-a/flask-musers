# -*- coding: utf-8 -*-

from functools import wraps

from mongoengine import Document, EmailField, StringField, BooleanField, queryset_manager

from passlib.hash import pbkdf2_sha256
from passlib.utils import consteq


class UserError(Exception):
    pass


class NotAllowedError(UserError):
    pass


def is_allowed(func):
    """Check user password, when is correct, then run decorated function.

    :returns: decorated function

    """
    @wraps(func)
    def _is_allowed(user, *args, **kwargs):
        password = kwargs.pop('password', None)
        if user.check_password(password):
            return func(user, *args, **kwargs)
        else:
            raise NotAllowedError()

    return _is_allowed


class User(Document):
    email = EmailField(required=True, unique=True)
    _password = StringField()
    name = StringField()
    activated = BooleanField(default=False)

    @queryset_manager
    def active(doc_cls, queryset):
        return queryset.filter(activated=True)

    def __str__(self):
        return self.email

    def __repr__(self):
        return str(self)

    # def get_absolute_url(self):
    #     pass

    def set_password(self, password):
        self._password = pbkdf2_sha256.encrypt(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self._password)

    @is_allowed
    def change_email(self, mail):
        self.email = mail
        self.save()

    def is_active(self):
        return self.activated

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        # if not hasattr(self, '_authenticated'):
            # self._authenticated = False

        # return self._authenticated
        return True

    def get_id(self):
        return str(self.pk) if self.pk else None

    @classmethod
    def register(cls, email, password, activated=False, name=''):
        user = cls()
        user.email = email
        user.name = name
        user.activated = activated
        user.set_password(password)
        user.save()

        return user

    @classmethod
    def get_user(cls, email, password):
        try:
            user = cls.active.get(email=email)
            if not user.check_password(password):
                raise UserError()
        except cls.DoesNotExist:
            raise UserError()
        return user

    @classmethod
    def get_active_user_by_pk_or_none(cls, userid):
        try:
            user = cls.active.get(pk=userid)
        except cls.DoesNotExist:
            user = None
        return user
