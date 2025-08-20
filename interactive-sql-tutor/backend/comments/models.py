from django.db import models
from django.conf import settings

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    problem_id = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Comment"
        managed = False 

    def __str__(self):
        return f"Comment by {self.user.email} on Problem {self.problem_id}"