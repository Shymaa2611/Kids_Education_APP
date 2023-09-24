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
        return self.content

class Challenge(models.Model):
    title=models.CharField(max_length=25)
    image=models.ImageField(upload_to='challenges/',blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    content=models.ManyToManyField(Content,blank=True,null=True)
    def __str__(self):
        return self.title

