from django.db import models
from django.utils import timezone
from extensions.utils import gregorian_to_jalali


class Category(models.Model):
    
    title = models.CharField(max_length=200, verbose_name='عنوان دسته‌بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس دسته‌بندی')
    status = models.BooleanField(default=True, verbose_name='آیا نمایش داده شود؟')
    
    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
        ordering = ['title']

    def __str__(self):
        return self.title

class Post(models.Model):
    
    title = models.CharField(max_length=200, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس اختصاصی')
    category = models.ManyToManyField(Category, verbose_name='دسته‌بندی', related_name='posts')
    body = models.TextField(verbose_name='متن مقاله')
    thumbnail = models.ImageField(upload_to='post/images', verbose_name='تصویر مقاله')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')
    status = models.CharField(max_length=1, choices=(('d', 'پیش‌نویس'), ('p', 'منتشرشده')), default='d', verbose_name='وضعیت انتشار')
    
    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست‌ها'
        ordering = ['-publish']
    
    def __str__(self):
        return self.title
    
    def jpublish(self):
        return gregorian_to_jalali(self.publish)
    jpublish.short_description = 'زمان انتشار'
    
    def jcreated(self):
        return gregorian_to_jalali(self.created)
    jcreated.short_description = 'زمان ایجاد'
    
    def jupdated(self):
        return gregorian_to_jalali(self.updated)
    jupdated.short_description = 'زمان ویرایش'
