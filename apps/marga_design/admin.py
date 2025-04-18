from django.contrib import admin
from django.utils.html import format_html
from .models import Project, ProjectImage, Parameter, ProjectParameter, Application, BlogPost, BlogPostImage


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    search_fields = ['title']
    list_per_page = 10


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    readonly_fields = ['image_preview']
    max_num = 10

    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html(
                '<a href="{0}" target="_blank">'
                '<img src="{0}" style="max-width: 150px; max-height: 150px; margin: 5px;" />'
                '</a>', obj.image.url
            )
        return "Нет изображения"

    image_preview.short_description = "Превью изображения"


class ProjectParameterInline(admin.TabularInline):
    model = ProjectParameter
    extra = 1
    max_num = 10
    autocomplete_fields = ['parameter']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ['created']
    search_fields = ['title']
    inlines = [ProjectParameterInline, ProjectImageInline]
    list_display = ['title', 'price', 'published', 'top_rating']
    list_editable = ['published', 'top_rating']
    list_per_page = 10
    save_on_top = True
    ordering = ['-created']
    list_filter = ['published', 'price']
    fields = ['title', 'location', 'top_rating', 'price', 'published', 'description', 'created', 'plan_image']
    actions = ['on_published', 'off_published']

    @admin.action(description='Снять с публикации')
    def off_published(self, request, queryset):
        count = queryset.update(published=False)
        self.message_user(
            request,
            f'Было снято с публикации {count} проектов')

    @admin.action(description='Опубликовать')
    def on_published(self, request, queryset):
        count = queryset.update(published=True)
        self.message_user(
            request,
            f'Было опубликовано {count} проектов'
        )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'answer', 'created', 'updated', 'email', 'phone']
    list_editable = ['answer']
    fields = ['name', 'created', 'updated', 'answer', 'email', 'phone', 'message', 'note']
    readonly_fields = ['created', 'updated', 'message']
    list_filter = ['created', 'updated', 'answer']
    search_fields = ['name', 'email', 'phone']
    ordering = ['-created']
    list_per_page = 10


class BlogPostImageline(admin.TabularInline):
    model = BlogPostImage
    extra = 1
    max_num = 10
    autocomplete_fields = ['blog_post']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'published']
    list_editable = ['published']
    fields = ['title', 'slug', 'description', 'created', 'published']
    readonly_fields = ['created']
    list_filter = ['created', 'published']
    search_fields = ['title']
    ordering = ['-created']
    list_per_page = 10
    save_on_top = True
    inlines = [BlogPostImageline]
