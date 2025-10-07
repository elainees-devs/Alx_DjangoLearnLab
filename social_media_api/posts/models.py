from django.db import models
from django.conf import settings

User=settings.AUTH_USER_MODEL

class Post(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=120)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-created_at']

    def __str__(self):
        return f"{self.title} by {self.user.author}"
    
class Comment(models.Model):
    post=models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.post_id}"
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # Prevent duplicate likes
