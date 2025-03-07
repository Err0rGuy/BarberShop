import re
from rest_framework.exceptions import ValidationError

# Users passwords strength validator
def password_validator(value):
    if len(value) < 8:
        raise ValidationError('Password must contain at least 8 character.')
    if not re.search(r'[A-Z]', value):
        raise ValidationError('Password must contain at least one Uppercase.')
    if not re.search(r'[a-z]', value):
        raise ValidationError('Password must contain at least one Lowercase.')
    if not re.search(r'[0-9]', value):
        raise ValidationError('Password must contain at least one digit.')
    if not re.search(r'[@#!*%?&]', value):
        raise ValidationError('Password must contain at least one special character(@#!*%?&).')
