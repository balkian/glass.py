from django.contrib import admin

from push_notifications.admin import DeviceAdmin
from .models import Glass

admin.site.register(Glass, DeviceAdmin)
