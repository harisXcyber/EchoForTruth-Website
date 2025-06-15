# core/models.py

from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(max_length=400)
    thumbnail = models.URLField(help_text="Paste an image URL")
    source = models.CharField(max_length=100, blank=True, help_text="e.g., YouTube, AlMaghrib, etc.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
