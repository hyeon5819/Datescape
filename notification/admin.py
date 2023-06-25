from django.contrib import admin
from notification.models import Notification
from users.admin import CommonModelAdmin

# Register your models here.


class NotificationAdmin(CommonModelAdmin):
    fields = ("target_user", "type", "type_id")
    list_display = ("target_user", "type", "type_id")


admin.site.register(Notification, NotificationAdmin)
