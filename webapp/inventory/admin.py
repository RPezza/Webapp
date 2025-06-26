from django.contrib import admin
from .models import Booking, Asset
from django.contrib import admin
from .models import Booking
from .forms import BookingForm

admin.site.register(Asset)

class BookingAdmin(admin.ModelAdmin):
    form = BookingForm
    list_display = ('asset', 'start_date', 'end_date', 'purpose', 'user')
    list_filter = ('start_date', 'end_date', 'asset')
    search_fields = ('asset__name', 'user__username', 'purpose')
    ordering = ('-start_date',)

admin.site.register(Booking, BookingAdmin)

from django.contrib import admin
from .models import UserMessage

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'timestamp', 'message')
    search_fields = ('name', 'email', 'subject', 'message')
