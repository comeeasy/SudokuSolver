from django.db import models

# Create your models here.
class Image(models.Model):
    sudoku_image = models.ImageField(upload_to="img/")
    sudoku_image_result = models.ImageField(upload_to="result/", null=True, blank=True)