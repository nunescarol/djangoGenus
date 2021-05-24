from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from polymorphic.models import PolymorphicModel

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .fields import OrderField

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(User,related_name='courses_created', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, default='')
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
        
class Module(PolymorphicModel):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # order = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return self.title

    # def __str__(self):
    #     return '{}. {}'.format(self.order, self.title)
    
    class Meta:
        ordering = ('-created',)

    # class Meta:
    #     ordering = ['order']

class Post(Module):
    module = models.ForeignKey(Module,related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Activity(Module):
    module = models.ForeignKey(Module,related_name='activities', on_delete=models.CASCADE)
    grade = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, limit_choices_to={'model__in':('text', 'video', 'image', 'file')}, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')


class ItemBase(models.Model):
    owner = models.ForeignKey(User,related_name='%(class)s_related', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return self.title

    def render(self):
        return render_to_string('content/{}.html'.format(self._meta.model_name), {'item': self})

class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.CharField(max_length=255)
    #models.ForeignKey(User,related_name='author_id', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    #approved_comment = models.BooleanField(default=False) 
        #para moderação no futuro

    #def approve(self):
    #    self.approved_comment = True
    #    self.save()
    def __str__(self):
        return '%s - %s' % (self.post.title, self.author)
        #mostrar no admin o post e o comentario associado a ele