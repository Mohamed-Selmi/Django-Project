from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
UserModel = get_user_model()



def validate_email(data):
    email = data['email'].strip()
    if not email:
        raise ValidationError('an email is needed')
    return True