from django.contrib import admin
from . import models
from .views import start_auth, confirm_code
from django.urls import path
from django.shortcuts import redirect


@admin.register(models.Account)
class UserAdmin(admin.ModelAdmin):
    exclude = [
        'phone_code_hash',
        'session_string'
    ]
    readonly_fields = [
        'created_date',
        'last_auth'
    ]
    search_fields = [
        'name',
        'is_active',
        'is_banned',
    ]
    list_filter = ['is_active', 'name', 'is_banned']
    list_display = ['name', 'is_active', 'last_auth', 'phone_number', 'created_date', 'is_banned']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # если объект уже существует (редактирование)
            return ['api_id', 'api_hash', 'phone_number', 'created_date', 'last_auth']
        else:  # если объект создается
            return ['created_date', 'last_auth', 'is_active', 'is_banned']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('start-auth/<uuid:account_id>/', self.admin_site.admin_view(start_auth), name='start-auth'),
            path('confirm-code/', self.admin_site.admin_view(confirm_code), name='confirm-code')
        ]
        return custom_urls + urls

    def start_auth_view(self, request, obj):
        return redirect('admin:start-auth', account_id=obj.id)

    def response_change(self, request, obj):
        if "_start-auth" in request.POST and obj.is_active:
            return self.start_auth_view(request, obj)
        return super().response_change(request, obj)

    change_form_template = "admin/api/account/change_form.html"


@admin.register(models.Chat)
class AddressAdmin(admin.ModelAdmin):
    readonly_fields = [
        'chat_id',
        'account',
        'last_message_send',
        'is_banned',
        'title'
    ]
    search_fields = [
        'account',
        'title',
        'is_active'
    ]
    list_filter = ['is_active', 'title', 'account__name', 'is_banned']
    list_display = ['title', 'account', 'last_message_send', 'is_active', 'is_banned']

    def has_add_permission(self, request):
        return False


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    search_fields = [
        'message_type'
    ]
    list_display = ['message_type']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # если объект уже существует (редактирование)
            return ['message_type']
        else:  # если объект создается
            return []


@admin.register(models.Interval)
class MessageAdmin(admin.ModelAdmin):
    search_fields = [
        'account'
    ]
    list_display = ['account', 'interval']
    list_filter = ['account__name']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # если объект уже существует (редактирование)
            return ['account']
        else:  # если объект создается
            return []
