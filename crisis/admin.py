from django.contrib import admin

# Register your models here.
from crisis.models import Participant, Crisis


class ParticipantModelAdmin(admin.ModelAdmin):
    pass


class CrisisModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Participant, ParticipantModelAdmin)
admin.site.register(Crisis, CrisisModelAdmin)
