# -*- coding: utf-8 -*-

from mongoengine import Document, EmailField, StringField, BooleanField, queryset_manager

from passlib.hash import pbkdf2_sha256
from passlib.utils import consteq


class UserError(Exception):
    pass


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

    def is_active(self):
        return self.activated

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        #if not hasattr(self, '_authenticated'):
            #self._authenticated = False

        #return self._authenticated
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
