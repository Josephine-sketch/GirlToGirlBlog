from django.db import models
from django.utils import timezone
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["timestamp"]
        
    def is_archived(self):
        return self.created < (timezone.now() - timezone.timedelta(days=14))
    
    def total_likes(self):
        return self.likes.count()
     
    def is_popular(self):
        return self.likes.count() > 2

class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.user.username} on {self.post.title}"
    
    class Meta:
        ordering = ['-created_at']