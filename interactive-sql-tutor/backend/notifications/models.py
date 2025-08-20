from django.db import models
from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Meta:
    db_table = "Notification"
    managed = False
    
    def __str__(self):
        # Display first 20 characters of the message
        return f"Notification for {self.user.username}: {self.message[:20]}"