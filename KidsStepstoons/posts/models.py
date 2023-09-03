from django.db import models
from django.urls import reverse
from accounts.models import User
from django.utils import timezone
from django.utils.html import format_html


from extensions.utils import gregorian_to_jalali


class PostManager(models.Manager):
    
    def published(self):
        return self.filter(status="p")

class CategoryManager(models.Manager):
    
    def active(self):
        return self.filter(status=True)


class Category(models.Model):
    
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name='زیردسته')
    title = models.CharField(max_length=200, verbose_name='عنوان دسته‌بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس دسته‌بندی')
    status = models.BooleanField(default=True, verbose_name='آیا نمایش داده شود؟')
    psition = models.IntegerField(unique=True, verbose_name='موقعیت')
    
    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
        ordering = ['parent__id', 'psition']

    def __str__(self):
        return self.title
    
    objects = CategoryManager()

class Post(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='نویسنده', null=True, related_name='posts')    
    title = models.CharField(max_length=200, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس اختصاصی')
    category = models.ManyToManyField(Category, verbose_name='دسته‌بندی', related_name='posts')
    body = models.TextField(verbose_name='متن مقاله')
    thumbnail = models.ImageField(upload_to='post/images', verbose_name='تصویر مقاله')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')
    status = models.CharField(max_length=1, choices=(('d', 'پیش‌نویس'), ('p', 'منتشرشده'), ('i', 'در حال بررسی'), ('b', 'برگشت داده شده')), default='d', verbose_name='وضعیت انتشار')
    is_special = models.BooleanField(default=False, verbose_name='مقاله ویژه')
    
    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست‌ها'
        ordering = ['-publish']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("dashboard:posts")
    
    def jpublish(self):
        return gregorian_to_jalali(self.publish)
    jpublish.short_description = 'زمان انتشار'
    
    def jcreated(self):
        return gregorian_to_jalali(self.created)
    jcreated.short_description = 'زمان ایجاد'
    
    def jupdated(self):
        return gregorian_to_jalali(self.updated)
    jupdated.short_description = 'زمان ویرایش'
    
    def thumbnail_tag(self):
        return format_html('<img src="{}" width="80" hight="50" />'.format(self.thumbnail.url))
    thumbnail_tag.short_description = 'عکس'
    
    def category_to_str(self):
        return ", ".join([category.title for category in self.category.all()])
    category_to_str.short_description = 'دسته‌بندی‌ها'
    
    objects = PostManager()