from django.contrib import admin

# Register your models here.
from django.contrib.gis.db import models
from django.forms import widgets

from crisis.models import Participant, Crisis


class ParticipantModelAdmin(admin.ModelAdmin):
    pass
    # formfield_overrides = {
    #     models.PointField: {'widget': widgets.TextInput()},
    # }


class CrisisModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Participant, ParticipantModelAdmin)
admin.site.register(Crisis, CrisisModelAdmin)
