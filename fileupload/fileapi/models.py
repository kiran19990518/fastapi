from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')

class ProcessedFile(models.Model):
    uploaded_file = models.OneToOneField(UploadedFile, on_delete=models.CASCADE)
    text = models.TextField()
    numbers = models.TextField()
    is_words = models.TextField()
