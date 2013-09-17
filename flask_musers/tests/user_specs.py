# -*- coding: utf-8 -*-


from should_dsl import should, should_not

from flask_musers.models import User
from tests.base import Spec


class UserSpec(Spec):
    def before(self):
        self.password = u'{*Y<IZ+Uxl'

        self.user = User()
        self.user.email = u'exm@example.com'
        self.user.set_password(self.password)
        self.user.first_name = u'Jožin'
        self.user.last_name = u'Zbažin'
        self.user.save()

    def should_not_save_another_user_with_same_email(self):
        from mongoengine.document import NotUniqueError

        u = User()
        u.email = self.user.email
        u.set_password(u'12345678')
        #u.save()

        lambda: u.save() |should| throw(NotUniqueError)

        #u.email |should_not| equal_to(self.user.email)

    def should_not_store_password_in_plain_text(self):
        self.user._password |should_not| equal_to(self.password)

    def should_return_id_as_unicode(self):
        self.user.get_id() |should| be_kind_of(unicode)

    def should_return_only_active_users(self):
        User.active() |should| be_empty

        self.user.activated = True
        self.user.save()

        len(User.active()) |should| be(1)

        u = User.active()[0]
        u.is_active() |should| be(True)

    def should_respond_to_set_password(self):
        self.user |should| respond_to('set_password')

    def should_respond_to_is_active(self):
        self.user |should| respond_to('is_active')

    def should_respond_to_is_authenticated(self):
        self.user |should| respond_to('is_authenticated')

    def should_respond_to_is_anonymous(self):
        self.user |should| respond_to('is_anonymous')

    def should_respond_to_get_id(self):
        self.user |should| respond_to('get_id')

    def should_check_for_right_password(self):
        self.user.check_password(self.password) |should| be(True)

    def should_check_for_wrong_password(self):
        self.user.check_password('1234908078ewd') |should_not| be(True)
