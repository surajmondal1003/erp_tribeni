from django.db import models

# Create your models here.

class MailTemplate(models.Model):
    name=models.CharField(max_length=255)
    code=models.CharField(max_length=255)
    subject=models.CharField(max_length=255)
    html_content=models.TextField()
    text_content=models.TextField()

    def __str__(self):
        return self.name