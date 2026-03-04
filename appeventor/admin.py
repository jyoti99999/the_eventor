from django.contrib import admin
from .models import datadesire, adminuser, user_query, reservation, Event, Seat, ChatMessage

# Register your models here.
admin.site.register(datadesire)
admin.site.register(adminuser)
admin.site.register(user_query)
admin.site.register(reservation)

# new feature models
admin.site.register(Event)
admin.site.register(Seat)
admin.site.register(ChatMessage)
