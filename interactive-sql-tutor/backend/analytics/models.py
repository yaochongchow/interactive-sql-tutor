from django.db import models
from django.conf import settings
from admin_tools.models import SQLProblem  # or wherever SQLProblem is defined

class Meta:
    db_table = "LearningAnalytics"
    managed = False
    
class ProblemAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey(SQLProblem, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    attempt_time = models.DateTimeField(auto_now_add=True)