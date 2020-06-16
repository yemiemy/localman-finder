from django.db import models
from django.conf import settings 
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):

        return self.name


class Place(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='pictures/%Y/%m/%d/', max_length=255, null=True, blank=True)
    description = RichTextUploadingField()
    address = models.TextField()
    location = models.CharField(max_length=120, blank=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name='places', null=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(
        default='',
        editable=False,
        max_length=120,
    )
    date_stamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'slug')

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('place-list', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
    

class Feedback(models.Model):
    fname = models.CharField(max_length=120)
    lname = models.CharField(max_length=120)
    image = models.ImageField(upload_to='feedbacks/%Y/%m/%d/', null=True, blank=True)
    message = RichTextUploadingField()
    date_stamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.fname

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Contact(models.Model):
    fname = models.CharField(max_length=120)
    lname = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    subject = models.CharField(max_length=150)
    message = models.TextField(blank=True, null=True)
    date_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fname
    