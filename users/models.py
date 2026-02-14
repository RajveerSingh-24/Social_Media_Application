from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import pyotp

# Create your models here.
class User(AbstractUser):
<<<<<<< HEAD
    email = models.EmailField(unique=True)
=======
    email = models.EmailField(unique=True,)
>>>>>>> e5dec9e (Updated models.py)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
    upload_to='profile_pics/',
    blank=True,
    null=True
)


    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        through='Follow',
        through_fields=('follower', 'following'),
        blank=True
    )

    is_2fa_enabled = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=32, blank=True, null=True)

    def generate_otp_secret(self):
        self.otp_secret = pyotp.random_base32()
        self.save()

    def get_totp_uri(self):
        return pyotp.totp.TOTP(self.otp_secret).provisioning_uri(
            name=self.email,
            issuer_name="SocialMediaSaaS"
        )

    def verify_otp(self, otp):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(otp)

    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        through='Follow',
        through_fields=('follower', 'following'),
        blank=True
    )

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following_set',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='followers_set',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_follow')
        ]

    def __str__(self):
        return f"{self.follower} follows {self.following}"
