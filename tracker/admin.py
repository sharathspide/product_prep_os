from django.contrib import admin
from .models import Phase, Chapter, Problem, StudySession

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0

@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ('order','title','target_days')
    inlines = [ChapterInline]

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title','phase','order')

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title','chapter','difficulty','points','completed','next_review_at')
    list_filter = ('difficulty','completed','chapter__phase')
    search_fields = ('title','notes')

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('date','minutes','problems_solved')
