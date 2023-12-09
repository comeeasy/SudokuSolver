from django.conf import settings
from django.db import models

class Image(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=0
    )
    sudoku_image = models.ImageField(upload_to="img/")
    sudoku_image_result = models.ImageField(upload_to="result/", null=True, blank=True)
