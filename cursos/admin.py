from django.contrib import admin
from django.db.models import Q

# Register your models here.


from django.contrib import admin
from .models import Subject, Course, Module, Activity
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    
class ModuleInline(admin.StackedInline):
    model = Module

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        # ModelA.objects.not_instance_of(ModelB [, ModelC ...])
        return qs.filter( Q(not_instance_of=Activity) )

class ActivityInline(admin.StackedInline):
    model = Activity


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline, ActivityInline]

# @admin.register(Activity)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ['title', 'subject', 'created']
#     list_filter = ['created', 'subject']
#     search_fields = ['title', 'overview']
#     prepopulated_fields = {'slug': ('title',)}
#     inlines = [ModuleInline]