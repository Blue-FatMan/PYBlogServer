from django.contrib import admin
from . import models
from blog.tools.common import get_current_time


# Register your models here.


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_time', 'update_time')

    readonly_fields = ('create_time', 'update_time')

    def save_model(self, request, obj, form, change):
        current_time = get_current_time()
        if change:  # 更改的时候
            obj.update_time = current_time
        else:  # 新增的时候
            obj.create_time = current_time
            obj.update_time = current_time
        super(TagAdmin, self).save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        # 禁止从admin中删除
        return False


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_time', 'update_time')

    readonly_fields = ('create_time', 'update_time')

    def save_model(self, request, obj, form, change):
        current_time = get_current_time()
        if change:  # 更改的时候
            obj.update_time = current_time
        else:  # 新增的时候
            obj.create_time = current_time
            obj.update_time = current_time
        super(CategoryAdmin, self).save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        # 禁止从admin中删除
        return False


@admin.register(models.BlogContent)
class BlogContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'create_time', 'update_time')

    readonly_fields = ('create_time', 'update_time')

    def save_model(self, request, obj, form, change):
        current_time = get_current_time()
        if change:  # 更改的时候
            obj.update_time = current_time
        else:  # 新增的时候
            obj.create_time = current_time
            obj.update_time = current_time
        super(BlogContentAdmin, self).save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        # 禁止从admin中删除
        return False


@admin.register(models.BlogDownloadContent)
class BlogDownloadContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_site', 'source_url', 'local_path', "create_time", "update_time")

    readonly_fields = ('create_time', 'update_time')

    def save_model(self, request, obj, form, change):
        current_time = get_current_time()
        if change:  # 更改的时候
            obj.update_time = current_time
        else:  # 新增的时候
            obj.create_time = current_time
            obj.update_time = current_time
        super(BlogDownloadContentAdmin, self).save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        # 禁止从admin中删除
        return False


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'description', 'blog_from', 'categories', "tags", "content_id", "create_time", "update_time")

    readonly_fields = ('create_time', 'update_time')

    def save_model(self, request, obj, form, change):
        current_time = get_current_time()
        if change:  # 更改的时候
            obj.update_time = current_time
        else:  # 新增的时候
            obj.create_time = current_time
            obj.update_time = current_time
        super(BlogAdmin, self).save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        # 禁止从admin中删除
        return False
