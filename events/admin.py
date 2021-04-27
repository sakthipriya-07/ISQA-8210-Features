from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Event, User, Customer

from django.shortcuts import render
from .forms import SendEmailForm
from django.core.exceptions import ObjectDoesNotExist

class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ['title', 'day', 'start_time', 'end_time', 'notes']


admin.site.register(Event, EventAdmin)


def send_email(self, request, queryset):
    form = SendEmailForm(initial={'users': queryset[0].user})
    return render(request, 'send_email.html', {'form': form})


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['username', 'is_customer', 'phone']


class CustomerAdmin(admin.ModelAdmin):

    list_display = ('user', 'first_name', 'last_name', 'email', 'phone')

    def username(self, instance):  # name of the method should be same as the field given in `list_display`
        try:

            return instance.user.username
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def first_name(self, instance):
        try:
            return instance.user.first_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def last_name(self, instance):
        try:
            return instance.user.last_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def email(self, instance):
        try:
            return instance.user.email
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def phone(self, instance):
        try:
            return instance.user.phone
        except ObjectDoesNotExist:
            return 'ERROR!!'

    actions = [send_email]


admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
