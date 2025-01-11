from django.core.validators import RegexValidator
from django.db import models


class Author(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, null=True)
    author_profile = models.ImageField(upload_to="Media/author")
    # name = models.CharField(max_length=100, null=True, validators=[
    #     RegexValidator(regex='^[a-zA-Z]+$', message='Name must only contain alphabetic characters.',
    #         code='invalid_name')])
    about_author = models.TextField()
    profession = models.CharField(max_length=100, null=True,)

    def __str__(self):
        return self.user.username
