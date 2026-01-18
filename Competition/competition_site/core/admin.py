from django.contrib import admin
from .models import Competition, Participant


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'key')


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'competition')
