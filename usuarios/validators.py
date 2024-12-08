import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class MinimumSpecialCharactersValidator:
    def __init__(self, min_special_chars=1):
        self.min_special_chars = min_special_chars

    def validate(self, password, user=None):
        special_characters = re.findall(r"[!@#$%^&*(),.?\":{}|<>]", password)
        if len(special_characters) < self.min_special_chars:
            raise ValidationError(
                _(f"La contraseña debe contener al menos {self.min_special_chars} carácter(es) especial(es)."),
                code='password_no_special_char',
            )

    def get_help_text(self):
        return _(f"Tu contraseña debe contener al menos {self.min_special_chars} carácter(es) especial(es).")
