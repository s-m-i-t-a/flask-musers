import six
import pytest

from mock import patch, call, MagicMock, Mock

from blinker import signal
from bson.objectid import ObjectId
from mongoengine.errors import NotUniqueError

from flask_musers.models import (
    User,
    UserError,
    is_allowed,
    NotAllowedError,
    EmailNotFound,
    InvalidPassword,
    validate_password
)

from tests import validator


class TestUserModel(object):
    @pytest.mark.usefixtures("db")
    def test_user_register(self):
        email = 'jozin@zbazin.cz'
        password = 'Nevimvim_)12123'

        User.register(email=email, password=password, activated=True)

        u = User.objects.first()

        assert u.email == email
        assert u.check_password(password)
        assert u.activated

    @pytest.mark.usefixtures("db")
    def test_user_register_return_new_user_object(self):
        email = 'jozin@zbazin.cz'
        password = 'Nevimvim_)12123'

        u = User.register(email=email, password=password, activated=True)

        assert u.email == email
        assert u.check_password(password)
        assert u.activated

    @pytest.mark.usefixtures("db")
    def test_raise_error_when_user_register_again(self):
        email = 'jozin@zbazin.cz'
        password = 'Nevimvim_)12123'

        User.register(email=email, password=password, activated=True)
        with pytest.raises(NotUniqueError):
            User.register(email=email, password=password, activated=True)

    @pytest.mark.usefixtures("db")
    def test_get_id_return_string_when_object_is_saved(self):
        u = User.register(email='nevim@nevim.cz', password='Jedna_dva_3', activated=True)

        uid = str(u.pk)

        assert uid == u.get_id()

    @pytest.mark.usefixtures("app")
    def test_get_id_return_none_when_is_unsaved(self):
        u = User(email='nevim@nevim.cz', activated=True)
        u.set_password('Jedna_dva_3')

        assert u.get_id() is None

    @pytest.mark.usefixtures("db")
    def test_active_queryset_returns_only_active_users(self):
        for i in range(20):
            User.register(email='user%d@foo.cz' % i, password='pass]W_%d' % i, activated=i % 2 == 0)

        active_users = User.active.all()

        assert len(active_users) == 10
        assert all([u.activated for u in active_users])

    @pytest.mark.usefixtures("app")
    @patch('flask_musers.models.pbkdf2_sha256.encrypt')
    def test_encrypt_user_password(self, mock_encrypt):
        password = 'Nevimvim_)12123'
        u = User()
        u.set_password(password)

        assert mock_encrypt.called

        kall = call(password)
        assert mock_encrypt.call_args == kall

        assert u._password == mock_encrypt.return_value

    @patch('flask_musers.models.pbkdf2_sha256.encrypt')
    @patch('flask_musers.models.validate_password')
    def test_validate_password(self, mock_validate, mock_encrypt):
        password = 'Nevimvim_)12123'
        u = User()
        u.set_password(password)

        assert mock_validate.called
        assert mock_validate.call_args == call(password)

    def test_user_cant_be_anonymous(self):
        u = User()

        assert not u.is_anonymous()

    def test_user_is_always_authenticated(self):
        u = User()

        assert u.is_authenticated()

    def test_is_active_when_user_is_activated(self):
        u = User(activated=True)

        assert u.is_active()

    def test_object_text_representation(self):
        email = 'jozin@zbazin.cz'
        u = User(email=email)

        assert str(u) == email
        assert repr(u) == email

    @pytest.mark.usefixtures("db")
    def test_get_user_return_only_active_user(self):
        email = 'jozin@zbazin.cz'
        password = 'Nevimvim_)12123'

        User.register(email=email, password=password, activated=False)

        with pytest.raises(UserError):
            User.get_user(email=email, password=password)

    def test_get_user_raise_error_when_user_not_found(self):
        # raise UserError when user not found
        email = 'jozin@zbazin.cz'
        password = 'Nevimvim_)12123'

        with pytest.raises(UserError):
            User.get_user(email=email, password=password)

    @pytest.mark.usefixtures("db")
    def test_get_user_raise_error_when_password_is_wrong(self):
        # raise UserError when user not found
        email = 'jozin@zbazin.cz'
        password = 'Nevimvim_)12123'
        User.register(email=email, password=password, activated=True)

        with pytest.raises(UserError):
            User.get_user(email=email, password='asdasd')

    @pytest.mark.usefixtures("db")
    def test_get_user_return_user(self):
        email = 'jozin@zbazin.cz'
        password = 'Nevimvim_)12123'

        ur = User.register(email=email, password=password, activated=True)

        u = User.get_user(email=email, password=password)

        assert ur.pk == u.pk

    @pytest.mark.usefixtures("db")
    def test_get_active_user_by_pk_or_none_return_active_user(self):
        email = 'jozin@zbazin.cz'
        password = 'Nevimvim_)12123'

        ur = User.register(email=email, password=password, activated=True)

        u = User.get_active_user_by_pk_or_none(str(ur.pk))

        assert isinstance(u, User)
        assert u.pk == ur.pk

    @pytest.mark.usefixtures("db")
    def test_get_active_user_by_pk_or_none_return_none_when_user_is_inactive(self):
        email = 'jozin@zbazin.cz'
        password = 'Nevimvim_)12123'

        ur = User.register(email=email, password=password, activated=False)

        u = User.get_active_user_by_pk_or_none(str(ur.pk))

        assert u is None

    @pytest.mark.usefixtures("db")
    def test_get_active_user_by_pk_or_none_return_none_when_user_dont_exists(self):
        oid = ObjectId()
        u = User.get_active_user_by_pk_or_none(str(oid))

        assert u is None

    @pytest.mark.usefixtures("db")
    def test_change_email(self):
        email = 'jozin@zbazin.cz'
        new_email = 'new@mail.com'
        password = 'Nevimvim_)12123'

        user = User.register(email=email, password=password, activated=True)
        assert user.email == email

        user.change_email(new_email, password=password)

        user = User.get_active_user_by_pk_or_none(str(user.pk))
        assert user.email == new_email

    @pytest.mark.usefixtures("db")
    def test_emit_signal_after_email_change(self):
        email = 'jozin@zbazin.cz'
        new_email = 'new@mail.com'
        password = 'Nevimvim_)12123'

        user = User.register(email=email, password=password, activated=True)

        changed = signal('musers-email-changed')

        @changed.connect
        def catch_signal(user, data):
            catch_signal._called = True
            assert user.email == new_email
        catch_signal._called = False

        user.change_email(new_email, password=password)
        assert catch_signal._called, "Signal has not been captured"

    @pytest.mark.usefixtures("db")
    def test_change_email_signal_contains_new_and_old_email(self):
        email = 'jozin@zbazin.cz'
        new_email = 'new@mail.com'
        password = 'Nevimvim_)12123'

        user = User.register(email=email, password=password, activated=True)

        changed = signal('musers-email-changed')

        @changed.connect
        def catch_signal(user, data):
            catch_signal._called = True
            assert user.email == new_email
            assert data['new'] == new_email
            assert data['old'] == email
        catch_signal._called = False

        user.change_email(new_email, password=password)
        assert catch_signal._called, "Signal has not been captured"

    @pytest.mark.usefixtures("db")
    def test_change_password(self):
        email = 'jozin@zbazin.cz'
        password = 'Nevimvim_)12123'
        new_password = 'new_passW0rD'

        user = User.register(email=email, password=password, activated=True)

        user.change_password(new_password, password=password)

        user = User.get_active_user_by_pk_or_none(str(user.pk))
        assert user.check_password(new_password)

    @pytest.mark.usefixtures("db")
    def test_emit_signal_after_password_change(self):
        email = 'jozin@zbazin.cz'
        password = 'Nevimvim_)12123'
        new_password = 'new_passW0rD'

        user = User.register(email=email, password=password, activated=True)
        changed = signal('musers-password-changed')

        catch = MagicMock('catch_signal')
        changed.connect(catch)

        user.change_password(new_password, password=password)
        assert catch.called, "Signal has not been captured"
        assert catch.call_args == call(user)

    @pytest.mark.usefixtures("db")
    def test_find_by_email_return_user_when_found(self):
        email = 'jozin@zbazin.cz'
        password = 'Nevimvim_)12123'

        user = User.register(email=email, password=password, activated=True)

        u = User.get_by_email(email)

        assert u.pk == user.pk
        assert u.email == user.email
        assert u._password == user._password

    @pytest.mark.usefixtures("db")
    def test_raise_email_not_found(self):
        with pytest.raises(EmailNotFound):
            User.get_by_email('bad@email.com')


class TestIsAllowedDecorator(object):
    @pytest.mark.usefixtures("db")
    def test_allow_call_function(self):
        email = 'jozin@zbazin.cz'
        password = 'Nevimvim_)12123'

        @is_allowed
        def f(self):
            return self.get_id()

        User.f = f
        user = User.register(email=email, password=password, activated=True)

        assert user.f(password=password) == user.get_id()

    @pytest.mark.usefixtures("db")
    def test_call_not_allowed(self):
        email = 'jozin@zbazin.cz'
        password = 'Nevimvim_)12123'

        @is_allowed
        def f(self):
            return self.get_id()

        User.f = f
        user = User.register(email=email, password=password, activated=True)

        with pytest.raises(NotAllowedError):
            user.f(password='bad password')


class TestValidatePassword(object):
    def test_use_custom_validator_and_raise_error(self, app):
        app.config['MUSERS_PASSWORD_VALIDATOR'] = 'tests.bad_validator'
        with pytest.raises(InvalidPassword) as excinfo:
            validate_password('pass')

            assert excinfo.value.message == 'Error'

    def test_use_custom_validator(self, app):
        app.config['MUSERS_PASSWORD_VALIDATOR'] = 'tests.validator'
        validate_password('pass')

        assert validator.called
        assert validator.call_args == call('pass')
