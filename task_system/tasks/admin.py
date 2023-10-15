from django.contrib import admin
from task_system.tasks.models import Task, TaskComment


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "enable",
        "status",
    )
    search_fields = ("id", "name", "status")
    list_filter = (
        "status",
        "enable",
        "created_at",
        "created_by",
        "performer",
    )
    readonly_fields = ("created_by", "created_at", "updated_at")


class TaskCommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "task",
        "created_by",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("created_by", "created_at", "updated_at")
    list_filter = ("created_by", "created_at", "updated_at")
    search_fields = ("text",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("task", "created_by")


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskComment, TaskCommentAdmin)
