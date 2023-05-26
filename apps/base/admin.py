from django.contrib import admin
from .models import User, CustomUser


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'phone', 'first_name', 'last_name', 'city')
    # prepopulated_fields = {"slug": ("username",)}


admin.site.register(User, UserAdmin)
# admin.site.register(CustomUser)
