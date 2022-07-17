from django.contrib import admin

# Register your models here.

from .models import Notes,User
admin.site.register(Notes)

@admin.register(User)
class myUsers(admin.ModelAdmin):
    list_display=['id','name','email','password','date_joined']

