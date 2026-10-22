from django.contrib import admin
from .models import Document, InternProfile, InternSkill, Location, Skill


@admin.register(InternProfile)
class InternProfileAdmin(admin.ModelAdmin):
    list_display = ("intern_id", "full_name", "role", "work_mode", "status", "location")
    list_filter = ("role", "work_mode", "status", "employment_type")
    search_fields = ("intern_id", "full_name", "search_keywords")
    filter_horizontal = ("skills",)


admin.site.register(Document)
admin.site.register(Location)
admin.site.register(Skill)
admin.site.register(InternSkill)

# Register your models here.
