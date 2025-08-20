from django.db import models
from django.conf import settings

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon_url = models.URLField(blank=True, null=True)  # optional image

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)
    
class Meta:
    db_table = "Badge"
    managed = False

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"