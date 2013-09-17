# -*- coding: utf-8 -*-

from passlib.hash import pbkdf2_sha256
from passlib.utils import consteq

# XXX: Need a app.py file with db variable set to mongoengine :(
from app import db


class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    _password = db.StringField()
    first_name = db.StringField()
    last_name = db.StringField()
    activated = db.BooleanField(default=False)

    @db.queryset_manager
    def active(doc_cls, queryset):
        return queryset.filter(activated=True)

    def __unicode__(self):
        return self.email

    def get_absolute_url(self):
        pass

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
        return unicode(self.pk) if self.pk else None
