from django.forms import ValidationError
from .validations import validate_username
from django.contrib.auth import get_user_model, authenticate