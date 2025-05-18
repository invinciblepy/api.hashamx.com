from django.db import models



class Module(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    backend = models.CharField(max_length=100)
    type = models.CharField(max_length=100, null=True, blank=True)
    max_results = models.IntegerField(default=10)
    inputs = models.JSONField(default=dict, null=True)
    outputs = models.JSONField(default=dict, null=True)
    premium = models.BooleanField(default=False)
    repository = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


