from django.db import models
from django.contrib.auth.models import User
from .storage import ImageKitStorage

imagekit_storage = ImageKitStorage()

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    photo = models.ImageField(storage=imagekit_storage, upload_to='photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.text[:20]}'

    @property
    def photo_url(self):
        if self.photo:
            try:
                return self.photo.url
            except Exception:
                return str(self.photo)
        return None