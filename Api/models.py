from django.db import models

class Category(models.Model):
    category_title=models.CharField(max_length=25)
    image=models.ImageField(upload_to='categories/images/')
    def __str__(self):
        return self.category_title



