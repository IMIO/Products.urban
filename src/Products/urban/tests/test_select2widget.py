# -*- coding: utf-8 -*-
from Products.urban.widget.select2widget import Select2Widget
from mock import Mock, patch

import unittest


class TestSelect2Widget(unittest.TestCase):

    def test_view_list_value_does_not_raise(self):
        """Regression: list stored value no longer raises TypeError."""
        widget = Select2Widget()
        field = Mock()
        field.__name__ = "test_field"
        field.getAccessor.return_value.return_value = ["value1", "value2"]

        with patch(
            "Products.urban.widget.select2widget.resolve_vocabulary",
            return_value="value1, value2",
        ):
            result = widget.view(Mock(), field, Mock())
            self.assertEqual(result, "value1, value2")
