from django.contrib import admin

from tiers.models import Size, Tier


class TierDashboard(admin.ModelAdmin):
    list_display = ('name', 'link_flag', 'expired_link_flag')
    list_editable = ('link_flag', 'expired_link_flag')


class SizeDashboard(admin.ModelAdmin):
    list_display = ('id', 'height')
    list_editable = ('height', )


admin.site.register(Size, SizeDashboard)
admin.site.register(Tier, TierDashboard)
