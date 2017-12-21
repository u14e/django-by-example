from django.db import models
from django.contrib.auth.models import User
from uuslug import uuslug
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .fields import OrderField


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True, blank=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super().save(*args, **kwargs)


class Course(models.Model):
    owner = models.ForeignKey(User, related_name='courses_created')
    subject = models.ForeignKey(Subject, related_name='courses')

    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True, blank=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    students = models.ManyToManyField(User,
                                      related_name='courses_joined',
                                      blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super().save(*args, **kwargs)


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return '{}, {}'.format(self.order, self.title)


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents')
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to={
                                         'model__in': ('text',
                                                       'video',
                                                       'image',
                                                       'file')
                                     })
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    order = OrderField(blank=True, for_fields=['modules'])

    class Meta:
        ordering = ('order', )


class ItemBase(models.Model):
    """
    抽象Model: 各种类型的content
    """
    # 使用%(class)s使得相应的子类产生对应的related_name，如Text类：text_related
    owner = models.ForeignKey(User, related_name='%(class)s_related')
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def render(self):
        # self._meta.model_name 获取具体model的name，比如model: Image对应model_name: image
        return render_to_string('courses/content/{}.html'.format(self._meta.model_name),
                                {'item': self})

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()
