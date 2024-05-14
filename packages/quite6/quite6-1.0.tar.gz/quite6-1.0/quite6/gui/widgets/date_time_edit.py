import prett6
from .. import QDate
from .. import QDateTimeEdit
from .. import ui_extension
from .. import BaseInterface


@ui_extension
class DateTimeEdit(QDateTimeEdit, BaseInterface, prett6.WidgetStringInterface):
    class StringItem(prett6.WidgetStringItem):
        def __init__(self, parent: 'DateTimeEdit'):
            self.parent = parent

        def get_value(self):
            return self.parent.text()

        def set_value(self, value):
            value = value or ''
            self.parent.setDate(value)

        def set_changed_connection(self):
            # noinspection PyUnresolvedReferences
            self.parent.dateChanged.connect(self.string.check_change)
