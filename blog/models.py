from django.db import models
from django.conf import settings
from django.urls import reverse
from django.conf import settings 
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.utils.text import slugify
# Create your models here.

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):

        return self.name
        

class Post(models.Model):

    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=120
    )
    body = RichTextUploadingField()
    image = models.ImageField(upload_to='pictures/%Y/%m/%d/', max_length=255, null=True, blank=True)
    date_stamp = models.DateTimeField(auto_now_add=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(
        default='',
        editable=False,
        max_length=120,
    )

    def __str__(self):

        return "{} published on {}".format(self.title,self.date_stamp)

    class Meta:
        unique_together = ('title', 'slug')

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('single', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

class Comment(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    writer = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=120)
    website = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    active = models.BooleanField(default=True)
    date_stamp = models.DateTimeField(auto_now_add=True) 
    def __str__(self):

        return "{} commented under {} on {}".format(self.writer,self.post, self.date_stamp)
