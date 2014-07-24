import six
import pytest

if six.PY3:
    from unittest.mock import patch, call
else:
    from mock import patch, call

from flask_musers.models import User, UserError


class TestUserModel(object):
    @pytest.mark.usefixtures("db")
    def test_user_register(self):
        email = 'jozin@zbazin.cz'
        password = 'nevimvim_)12123'

        User.register(email=email, password=password, activated=True)

        u = User.objects.first()

        assert u.email == email
        assert u.check_password(password)
        assert u.activated

    @pytest.mark.usefixtures("db")
    def test_user_register_return_new_user_object(self):
        email = 'jozin@zbazin.cz'
        password = 'nevimvim_)12123'

        u = User.register(email=email, password=password, activated=True)

        assert u.email == email
        assert u.check_password(password)
        assert u.activated

    @pytest.mark.usefixtures("db")
    def test_get_id_return_string_when_object_is_saved(self):
        u = User.register(email='nevim@nevim.cz', password='jednadva3', activated=True)

        uid = str(u.pk)

        assert uid == u.get_id()

    def test_get_id_return_none_when_is_unsaved(self):
        u = User(email='nevim@nevim.cz', activated=True)
        u.set_password('jednadva3')

        assert u.get_id() is None

    @pytest.mark.usefixtures("db")
    def test_active_queryset_returns_only_active_users(self):
        for i in range(20):
            User.register(email='user%d@foo.cz' % i, password='passW%d' % i, activated=i % 2 == 0)

        active_users = User.active.all()

        assert len(active_users) == 10
        assert all([u.activated for u in active_users])

    @patch('flask_musers.models.pbkdf2_sha256.encrypt')
    def test_encrypt_user_password(self, mock_encrypt):
        password = 'nevimvim_)12123'
        u = User()
        u.set_password(password)

        assert mock_encrypt.called

        kall = call(password)
        assert mock_encrypt.call_args == kall

        assert u._password == mock_encrypt.return_value

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
        password = 'nevimvim_)12123'

        User.register(email=email, password=password, activated=False)

        with pytest.raises(UserError):
            User.get_user(email=email, password=password)

    def test_get_user_raise_error_when_user_not_found(self):
        # raise UserError when user not found
        email = 'jozin@zbazin.cz'
        password = 'nevimvim_)12123'

        with pytest.raises(UserError):
            User.get_user(email=email, password=password)

    @pytest.mark.usefixtures("db")
    def test_get_user_raise_error_when_password_is_wrong(self):
        # raise UserError when user not found
        email = 'jozin@zbazin.cz'
        password = 'nevimvim_)12123'
        User.register(email=email, password=password, activated=True)

        with pytest.raises(UserError):
            User.get_user(email=email, password='asdasd')

    @pytest.mark.usefixtures("db")
    def test_get_user_return_user(self):
        email = 'jozin@zbazin.cz'
        password = 'nevimvim_)12123'

        ur = User.register(email=email, password=password, activated=True)

        u = User.get_user(email=email, password=password)

        assert ur.pk == u.pk
