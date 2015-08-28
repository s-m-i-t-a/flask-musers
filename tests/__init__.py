# -*- coding: utf-8 -*-

from mock import Mock

validator = Mock(return_value=tuple())
bad_validator = Mock(return_value=('Error', ))
