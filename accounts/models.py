from django.db import models
import urllib.parse
from django.conf import settings
from django.db import models
import urllib.parse
from django.conf import settings

from django.db import models
import urllib.parse
from django.conf import settings
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import urllib.parse
from django.conf import settings

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name='email address', max_length=50, unique=True)
    username = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='profile_pictures', blank=True)
    password = models.CharField(max_length=128)  # Make sure to store the password hash here

    REQUIRED_FIELDS = []  #
    USERNAME_FIELD = 'email' 

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_picture_url(self):
        if self.picture:
            return urllib.parse.urljoin(settings.BASE_URL, self.picture.url)
        else:
            return None

    def set_password(self, raw_password):
        """Hashes and sets the password."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Checks if the raw password matches the hashed password."""
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def has_module_perms(self, app_label):
        return self.is_superuser  # Or customize as needed

    def has_perm(self, perm, obj=None):
        return self.is_superuser  # Or customize as needed

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"
