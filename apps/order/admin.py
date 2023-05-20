from django.contrib import admin
from .models import OrderItems, Order


class OrderItemsTabularInline(admin.TabularInline):
    readonly_fields = ('product', 'quantity', 'summa')
    model = OrderItems
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemsTabularInline]
    list_display = ('id', 'client', 'phone', 'get_quantity', 'get_summa', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('client__first_name', 'phone', 'address', 'note')
    readonly_fields = ('client', 'phone', 'address', 'zipcode', 'note', 'created_at',)


admin.site.register(OrderItems)
admin.site.register(Order, OrderAdmin)
