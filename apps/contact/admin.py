from django.contrib import admin
from .models import GetInTouch


class GetInTouchAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'email', 'created_at', 'finished')
    readonly_fields = ('full_name', 'phone', 'email', 'message', 'user_data', 'created_at')
    list_filter = ('finished', 'created_at')


admin.site.register(GetInTouch, GetInTouchAdmin)
