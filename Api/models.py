from django.db import models

class Category(models.Model):
    category_title=models.CharField(max_length=25)
    image=models.ImageField(upload_to='categories/images/')
    def __str__(self):
        return self.category_title


class Content(models.Model):
    content=models.CharField(max_length=200)
    kid_age=models.IntegerField(default=1)
    def __str__(self):
        return str(self.kid_age)
class Challenge(models.Model):
    title=models.CharField(max_length=25)
    image=models.ImageField(upload_to='challenges/')
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    content=models.ManyToManyField(Content)
    def __str__(self):
        return self.title

