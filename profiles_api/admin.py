from django.contrib import admin

from profiles_api import models

admin.site.register(models.UserProfile) # UserProfile is registered in admin site to use
