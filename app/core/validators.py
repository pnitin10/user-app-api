import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CharacterValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Za-z]', password):
            raise ValidationError(
                _("The password must contain at least 1 character, a-z or A-Z."),
                code='password_no_character',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 character, a-z or A-Z."
        )


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _("The password must contain at least 1 digit, 0-9."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 number, 0-9."
        )


class SymbolValidator:
    def validate(self, password, user=None):
        if not re.findall('[_#-]', password):
            raise ValidationError(
                _("The password must contain at least 1 symbol: " + "_ - #"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 symbol: " + "_-#")


class MaximumLengthValidator:
    def validate(self, password, user=None):
        if len(password) != 6:
            raise ValidationError(
                _("Password max length should be 6"),
                code='password_no_maximum_length',
            )

    def get_help_text(self):
        return _("Password max length should be 6")
