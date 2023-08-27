from django.contrib import admin
from .models import Post, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('psition', 'title', 'slug', 'parent', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'jcreated', 'jupdated', 'category_to_str')
    list_filter = ('status', 'created', 'updated')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status', '-publish']
    
    def category_to_str(self, obj):
        return ", ".join([category.title for category in obj.category.all()])
    category_to_str.short_description = 'دسته‌بندی‌ها'

admin.site.register(Post, PostAdmin)
