from django.contrib import admin
from .models import Place, Category, Feedback, Contact
# Register your models here.
admin.site.register(Place)
admin.site.register(Category)
admin.site.register(Feedback)
admin.site.register(Contact)