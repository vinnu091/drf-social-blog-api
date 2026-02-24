from django.contrib import admin
from .models import Blog,Comment,Follow

admin.site.register(Comment)
admin.site.register(Blog)
admin.site.register(Follow)

# Register your models here.
