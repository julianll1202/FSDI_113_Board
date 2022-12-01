from django.db import models
from django.contrib.auth import get_user_model, get_user
from django.urls import reverse

# Status model
class Status(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.name

# Priority model
class Priority(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.name

# Issue model
class Issue(models.Model):
    summary = models.CharField(max_length=256)
    description = models.TextField()
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        default=1
    )
    priority = models.ForeignKey(
        Priority,
        on_delete=models.CASCADE,
        default=1
    )
    reporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    assignee = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        related_name="assignee"
    )
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.summary[:500]
    
    def get_absolute_url(self):
        return reverse('detail', args=[self.id])

