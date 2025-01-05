from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify

from apps.instructor.models import Author


class Categories(models.Model):
    icon = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_categories():
        return Categories.objects.all().order_by('id')


class Level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language


class Course(models.Model):
    STATUS = (('PUBLISH', 'PUBLISH'), ('DRAFT', 'DRAFT'),)

    featured_image = models.ImageField(upload_to="Media/featured_img", null=True)
    title = models.CharField(
        max_length=500,
        validators=[
            RegexValidator(
                regex=r'^[^\d]*$',  # Regex to disallow numbers
                message='Title must not contain numbers.',
                code='invalid_title'
            )
        ]
    )
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    price = models.IntegerField(null=True, default=0)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100, null=True)

    def __str__(self):
        return self.title

    def get_slug(self):
        return reverse("course_details", kwargs={'slug': self.slug})


class what_to_learn(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points


class requirements(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    requirements = models.CharField(max_length=500)

    def __str__(self):
        return self.requirements


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " - " + self.course.title


class Video(models.Model):
    serial_number = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to="Media/Thumbnail")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    youtube_id = models.CharField(max_length=100, null=True)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    def __str__(self):
        return self.title


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, Course)
