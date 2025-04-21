from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user_full_name', 'phone', 'birth_date')
    fields = ('user', 'first_name', 'last_name', 'phone', 'address', 'birth_date', 'description')
    readonly_fields = ('first_name', 'last_name')

    @admin.display(description="Логин - имя пользователя")
    def get_user_full_name(self, obj):
        return f"{obj.user.username} - {obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username

    @admin.display(description="Имя")
    def first_name(self, obj):
        return obj.user.first_name

    @admin.display(description="Фамилия")
    def last_name(self, obj):
        return obj.user.last_name
