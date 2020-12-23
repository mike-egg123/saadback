from django.contrib import admin
from user.models import Profile, Follow, StarPaper

# Register your models here.
admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(StarPaper)