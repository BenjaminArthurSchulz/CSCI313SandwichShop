from django.contrib import admin
from .models import Coupon
# Register your models here.

#Coupon Admin
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_amount', 'is_active', 'expiration_date')
    search_fields = ('code',)