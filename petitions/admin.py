from django.contrib import admin

from petitions.models import Petition, Signature


@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    fields = ('title', 'body')
    list_display = ('title', 'body')


def make_active(modeladmin, request, queryset):
    queryset.update(active=True)
make_active.short_description = "Confirm selected signatures"


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    fields = ('name', 'affiliation', 'petition', 'active', 'initial',
            'timestamp')
    list_display = ('name', 'affiliation', 'petition', 'active', 'initial',
            'timestamp')
    list_filter = ('active', 'initial')
    search_fields = ['name', 'affiliation', 'email']
    actions = [make_active]



admin.site.site_title = 'IamWL Backend'
admin.site.site_header = 'IamWL Backend'
admin.site.site_url = None
