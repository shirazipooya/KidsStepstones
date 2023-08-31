from django.contrib import admin
from .models import Post, Category

admin.site.site_header = "مدیریت وبلاگ همقدم با کودک"

def make_published(modeladmin, request, queryset):
    rows_update = queryset.update(status='p')
    if rows_update == 1:
        message_bit = "منتشر شد."
    else:
        message_bit = "منتشر شدند."
    modeladmin.message_user(request, "{} مقاله {}".format(rows_update, message_bit))
make_published.short_description = "انتشار مقالات انتخاب شده"

def make_draft(modeladmin, request, queryset):
    rows_update = queryset.update(status='d')
    if rows_update == 1:
        message_bit = "پیش‌نویس شد."
    else:
        message_bit = "پیش‌نویس شدند."
    modeladmin.message_user(request, "{} مقاله {}".format(rows_update, message_bit))
make_draft.short_description = "پیش‌نویس شدن مقالات انتخاب شده"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('psition', 'title', 'slug', 'parent', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'slug', 'author', 'status', 'jcreated', 'jupdated', 'jpublish', 'category_to_str')
    list_filter = ('status', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status', '-publish']
    actions = [make_published, make_draft]

admin.site.register(Post, PostAdmin)
