from django.contrib import admin
from django.contrib.auth.models import User
from django.shortcuts import render

from .forms import SendEmailForm
from .models import Games, Reviews, Publisher, Categories, Profile


admin.site.register(Games)
admin.site.register(Reviews)
admin.site.register(Publisher)
admin.site.register(Categories)
admin.site.register(Profile)
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    actions = ['send_email', ]

    def send_email(self, request, queryset):
        form = SendEmailForm(initial={'users': queryset})

        return render(request, 'games/send_email.html', {'form': form})