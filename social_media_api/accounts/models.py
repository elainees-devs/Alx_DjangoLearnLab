from django.contrib.auth.models import AbstractUser

from django.db import models


class CustomUser(AbstractUser):
    bio=models.TextField(blank=True)
    profile_picture=models.ImageField(upload_to='profile_picture/', blank=True, null=True)
    following=models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def follow(self, user):
        if user == self:
            return
        self.following.add(user)

    def unfollow(self, user):
        if user == self:
            return
        self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(pk=user.pk).exists()

    def __str__(self):
        return self.username
    