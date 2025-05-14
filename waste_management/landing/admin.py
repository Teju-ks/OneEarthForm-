from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.utils.timezone import now
from twilio.rest import Client
from django.conf import settings
from .models import ProductSale, Buyer, Seller, OrganicProduct, OrganicManure, Order


@admin.register(ProductSale)
class ProductSaleAdmin(admin.ModelAdmin):
    list_display = ('seller', 'product_type', 'quantity', 'price_per_kg', 'total_earnings', 'date_sold')


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('username', 'city')  # Display username and city in the admin list view


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('username', 'city', 'notify_button')  # Add a custom button in the admin interface

    def notify_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Send Notification</a>',
            f'notify/{obj.pk}/'
        )

    notify_button.short_description = 'Notify Seller'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('notify/<int:seller_id>/', self.admin_site.admin_view(self.send_sms_notification), name='send_sms_notification'),
        ]
        return custom_urls + urls

    def send_sms_notification(self, request, seller_id):
        seller = Seller.objects.get(pk=seller_id)
        pickup_time = now().strftime("%Y-%m-%d %H:%M")
        message_body = f" OneEarthFarm - Dear {seller.username}, we are collecting your waste on {pickup_time}."

        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=message_body,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=seller.phone_number
            )
            self.message_user(request, f"SMS sent to {seller.username}", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Failed to send SMS: {e}", messages.ERROR)

        return redirect('..')


@admin.register(OrganicProduct)
class OrganicProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')  # Fields to display in the admin list view
    fields = ('name', 'description', 'price', 'stock')  # Include the image field


@admin.register(OrganicManure)
class OrganicManureAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')  # Fields to display in the admin list view
    fields = ('name', 'description', 'price', 'stock')  # Include the image field


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'quantity', 'price', 'city', 'state', 'order_date')
    list_filter = ('product_type', 'order_date', 'payment_method')
    search_fields = ('product_name', 'city', 'state')