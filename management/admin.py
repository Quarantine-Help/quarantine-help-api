from django.contrib import admin

from management.models import Ability


class AbilityModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ability, AbilityModelAdmin)
