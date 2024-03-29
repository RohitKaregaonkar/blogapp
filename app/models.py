from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    def save(self, *args,**kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField()
    slug = models.SlugField(max_length=120, unique=True)
    bio = models.CharField(max_length=200)
    
    def save(self, *args,**kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)
        return super(Profile, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.user.first_name
    


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    tags =  models.ManyToManyField(Tag, blank=True, related_name='post')
    view_count = models.IntegerField(null=True, blank=True)
    featured = models.BooleanField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    profiles = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    bookmarks = models.ManyToManyField(User, related_name='bookmarks', default=None, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', default=None, blank=True)
    
    def number_of_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title
    
    
    
class Comments(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=200)
    website = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='replies')
    
    
class Subscribe(models.Model):
    email = models.EmailField(max_length=120)
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email
    
    
class WebsiteMeta(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    about = models.TextField()