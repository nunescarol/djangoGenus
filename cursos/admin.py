from django.contrib import admin
from django.db.models import Q

# Register your models here.


from django.contrib import admin
from .models import Subject, Course, Module, Image, Content, Text, Video, Grade

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    
class ModuleInline(admin.StackedInline):
    model = Module

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     # if request.user.is_superuser:
    #     #     return qs
    #     # ModelA.objects.not_instance_of(ModelB [, ModelC ...])
    #     return qs.filter( Q(not_instance_of=Activity) )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created', 'id']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'module', 'grade']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'created', 'id']
    list_filter = ['created', 'course']
    # search_fields = ['title', 'overview']
    # prepopulated_fields = {'slug': ('title',)}
    # inlines = [ModuleInline, ActivityInline]

@admin.register(Content)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'item']
    list_filter = ['id']

@admin.register(Image)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created', 'id']
    list_filter = ['created', 'owner']

@admin.register(Text)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created', 'id']
    list_filter = ['created', 'owner']
    

@admin.register(Video)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created', 'id']
    list_filter = ['created', 'owner']

# @admin.register(Activity)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ['title', 'subject', 'created']
#     list_filter = ['created', 'subject']
#     search_fields = ['title', 'overview']
#     prepopulated_fields = {'slug': ('title',)}
#     inlines = [ModuleInline]